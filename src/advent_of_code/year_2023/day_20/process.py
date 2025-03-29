import abc
import collections
import enum
import dataclasses
import math


BUTTON = "button"
BROADCASTER = "broadcaster"
FINAL_MACHINE = "rx"

FLIP_FLOP_SYMBOL = "%"
CONJUNCTION_SYMBOL = "&"

CABLE_WARM_UP_NUMBER = 1000


class Pulse(enum.Enum):
    LOW = enum.auto()
    HIGH = enum.auto()


class ModuleState(enum.Enum):
    ON = enum.auto()
    OFF = enum.auto()

    def toggle(self):
        match self:
            case self.ON:
                return self.OFF
            case self.OFF:
                return self.ON


@dataclasses.dataclass(frozen=True)
class PulseMsg:
    pulse: Pulse
    source: str
    dest: str


class Module(abc.ABC):
    @abc.abstractmethod
    def output(self, input_: PulseMsg) -> list[PulseMsg] | None:
        pass


@dataclasses.dataclass
class BroadcasterModule(Module):
    name: str
    dests: list[str]

    def output(self, input_: PulseMsg) -> list[PulseMsg]:
        return [
            PulseMsg(pulse=input_.pulse, source=self.name, dest=dest)
            for dest in self.dests
        ]


@dataclasses.dataclass
class FlipFlopModule(Module):
    name: str
    dests: list[str]
    state: ModuleState = ModuleState.OFF

    PULSE_MAP = {ModuleState.ON: Pulse.HIGH, ModuleState.OFF: Pulse.LOW}

    def output(self, input_: PulseMsg) -> list[PulseMsg] | None:
        if input_.pulse == Pulse.HIGH:
            return None
        assert input_.pulse == Pulse.LOW
        self.state = self.state.toggle()
        output_pulse = self.PULSE_MAP[self.state]
        return [
            PulseMsg(pulse=output_pulse, source=self.name, dest=dest)
            for dest in self.dests
        ]


@dataclasses.dataclass
class ConjunctionModule(Module):
    name: str
    dests: list[str]
    pulse_history: dict[str:Pulse]

    def output(self, input_: PulseMsg) -> list[PulseMsg]:
        self.pulse_history[input_.source] = input_.pulse
        if all(pulse == Pulse.HIGH for pulse in self.pulse_history.values()):
            output_pulse = Pulse.LOW
        else:
            output_pulse = Pulse.HIGH
        return [
            PulseMsg(pulse=output_pulse, source=self.name, dest=dest)
            for dest in self.dests
        ]


class PulseRunner:
    def __init__(self, module_config):
        self.modules = {}
        self.conjunction_mods = {}
        for module_info in module_config.splitlines():
            name, dests_str = module_info.split(" -> ")
            dests = dests_str.split(", ")
            if name == BROADCASTER:
                self.modules[name] = BroadcasterModule(name=BROADCASTER, dests=dests)
            elif name.startswith(FLIP_FLOP_SYMBOL):
                name = name[1:]  # chop off symbol
                self.modules[name] = FlipFlopModule(name=name, dests=dests)
            elif name.startswith(CONJUNCTION_SYMBOL):
                name = name[1:]
                # pulse history cannot be established until the whole input is parsed
                # so default to empty for now
                self.modules[name] = ConjunctionModule(
                    name=name, dests=dests, pulse_history={}
                )
                self.conjunction_mods[name] = []
            else:
                raise ValueError("Unrecognised module type")

        # locate all conjunction mod inputs
        for module in self.modules.values():
            for dest in module.dests:
                if dest in self.conjunction_mods:
                    self.conjunction_mods[dest].append(module.name)

        # update conjunction mods with initialised pulse history for their inputs
        for name, dests in self.conjunction_mods.items():
            pulse_history = {dest_name: Pulse.LOW for dest_name in dests}
            self.modules[name].pulse_history = pulse_history

        self.is_special_input = None
        self.special_conjunction_mods = None
        self.special_conjunction_mod_cycle_1 = None
        self.special_conjunction_mod_cycle_2 = None
        self._assert_special_input()

        self.low_pulses = 0
        self.high_pulses = 0
        self.btn_count = 0

    def _assert_special_input(self):
        # Specially formed input means
        # 1. One conjunction module feeds the final machine only,
        #    and only one conjunction module feeds the final machine
        # 2. That conjunction module is fed by multiple other conjunction modules only
        # 3. Each one of the second-level conjunction modules is fed by one other conjunction module alone
        # 4. Each one the third-level conjunction modules are fed by flip-flop modules alone
        # 5. The three levels of conjunction modules are the only conjunction modules that exist
        #    (In other words, no conjunction modules feed flip-flop modules
        #    and the conjunction modules form a strict hierarchy.)
        #
        # These conditions mean that
        # All direct descendant flip-flop modules of third-level conjunction modules
        # must output high pulses simultaneously
        # So that all third-level conjunction modules must output low pulses simultaneously
        # So that the second-level conjunction modules output high pulses simultaneously
        # So that the top-level conjunction module outputs a low pulse to the final machine
        #
        # If you can prove then, that there is periodicity to third-level conjunction modules
        # outputting high pulses simultaneously
        # then those high pulses must occur at the same interval
        # each time as the above conditions means the result is deterministic
        # then the top-level conjunction module outputting a low pulse to the final machine
        # is just the lowest common multiple (LCM) of the min number of button presses
        # needed to make each third-level conjunction module output a low pulse

        # assertion 1
        top_level_conjunction_modules = []
        for name, module in self.modules.items():
            if module.dests == [FINAL_MACHINE]:
                top_level_conjunction_modules.append(name)
        if len(top_level_conjunction_modules) != 1:
            return False

        # assertion 2
        (top_level_conjunction_module,) = top_level_conjunction_modules
        second_level_conjunction_modules = self.conjunction_mods[
            top_level_conjunction_module
        ]
        for module in second_level_conjunction_modules:
            if module not in self.conjunction_mods:
                return False

        # assertion 3
        third_level_conjunction_modules = []
        for module in second_level_conjunction_modules:
            third_level_conjunction_module = self.conjunction_mods[module]
            if len(third_level_conjunction_module) != 1:
                return False
            (third_level_conjunction_module,) = third_level_conjunction_module
            third_level_conjunction_modules.append(third_level_conjunction_module)

        # assertion 4
        for module in third_level_conjunction_modules:
            third_level_conjunction_module_descs = self.conjunction_mods[module]
            for desc in third_level_conjunction_module_descs:
                if desc in self.conjunction_mods:
                    return False

        # assertion 5
        conjunction_modules = (
            top_level_conjunction_modules
            + second_level_conjunction_modules
            + third_level_conjunction_modules
        )
        self.is_special_input = len(conjunction_modules) == len(
            self.conjunction_mods
        ) and set(conjunction_modules) == set(self.conjunction_mods)

        if self.is_special_input:
            self.special_conjunction_mods = third_level_conjunction_modules
            self.special_conjunction_mod_cycle_1 = {
                mod: None for mod in self.special_conjunction_mods
            }
            self.special_conjunction_mod_cycle_2 = {
                mod: None for mod in self.special_conjunction_mods
            }

    def _find_special_conjunction_mod_periodicity(
        self,
        input_msg,
    ):
        if (
            input_msg.source in self.special_conjunction_mods
            and input_msg.pulse == Pulse.LOW
        ):
            if (
                current_result := self.special_conjunction_mod_cycle_1.get(
                    input_msg.source
                )
            ) is None or current_result == self.btn_count:
                self.special_conjunction_mod_cycle_1[input_msg.source] = self.btn_count
            else:
                self.special_conjunction_mod_cycle_2[input_msg.source] = self.btn_count

    def _attempt_calc_of_button_presses_to_turn_on_sand_machine(self):
        if all(
            count is not None for count in self.special_conjunction_mod_cycle_2.values()
        ):
            for mod in self.special_conjunction_mods:
                assert divmod(
                    self.special_conjunction_mod_cycle_2[mod],
                    self.special_conjunction_mod_cycle_1[mod],
                ) == (2, 0)
            return math.lcm(*self.special_conjunction_mod_cycle_1.values())
        return None

    def __iter__(self):
        return self

    def __next__(self):
        self.btn_count += 1
        pulse_q = collections.deque()
        pulse_history = []

        # initial broadcast
        init_msg = PulseMsg(pulse=Pulse.LOW, source=BUTTON, dest=BROADCASTER)
        pulse_q.appendleft(init_msg)

        while pulse_q:
            input_msg: PulseMsg = pulse_q.pop()
            if self.is_special_input:
                self._find_special_conjunction_mod_periodicity(
                    input_msg,
                )
                result = self._attempt_calc_of_button_presses_to_turn_on_sand_machine()
                if result is not None:
                    raise StopIteration(result)
            pulse_history.append(input_msg)
            match input_msg.pulse:
                case Pulse.LOW:
                    self.low_pulses += 1
                case Pulse.HIGH:
                    self.high_pulses += 1
            dest_mod = self.modules.get(input_msg.dest)
            if dest_mod is None:
                # untyped module found - no pulse sent
                continue
            output_msgs = dest_mod.output(input_msg)
            if output_msgs is None:
                continue
            for output_msg in output_msgs:
                pulse_q.appendleft(output_msg)

        return pulse_history


def read_file() -> str:
    with open("input.txt") as f:
        return f.read()


def main():
    input_ = read_file()

    pulse_runner = PulseRunner(input_)
    for _ in range(CABLE_WARM_UP_NUMBER):
        next(pulse_runner)
    print(
        f"Total number of low pulses times total number of high pulses after {CABLE_WARM_UP_NUMBER} button pushes:",
        pulse_runner.low_pulses * pulse_runner.high_pulses,
    )

    pulse_runner = PulseRunner(input_)
    while True:
        try:
            next(pulse_runner)
        except StopIteration as exc:
            button_presses_to_move_sand = exc.value
            break
    print(
        "Min num of button presses to turn on machine to move sand to Island Island:",
        button_presses_to_move_sand,
    )


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
