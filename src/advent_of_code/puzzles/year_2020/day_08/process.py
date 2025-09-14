import timeit


class HandheldHalting:
    def __init__(self, code_input=None):
        code_input = code_input if code_input is not None else self._read_file()
        self.code = self._preprocess(code_input)

    @staticmethod
    def _read_file():
        with open("input.txt") as f:
            return f.read()

    @staticmethod
    def _preprocess(code_input):
        code = []
        for inst in code_input.splitlines():
            op, arg = inst.split()
            code.append((op, int(arg)))
        return code

    def _process(self, code=None):
        code = code if code is not None else self.code
        visited = set()
        acc = 0
        pos = 0
        while True:
            if pos in visited:
                return "infinite loop", acc
            if pos == len(code):
                return "terminates", acc
            visited.add(pos)
            op, arg = code[pos]
            if op == "acc":
                acc += arg
                pos += 1
            elif op == "jmp":
                pos += arg
            elif op == "nop":
                pos += 1
            else:
                raise Exception

    def process(self):
        _, value = self._process()
        return value

    def process_with_changes(self):
        opp_swap = {"jmp": "nop", "nop": "jmp"}
        for pos, (opp, arg) in enumerate(self.code):
            if opp in opp_swap:
                new_opp = opp_swap[opp]
                code = self.code.copy()
                code[pos] = (new_opp, arg)
                termination_type, value = self._process(code)
                if termination_type == "terminates":
                    return value


def main():
    handheld_halting = HandheldHalting()
    print(f"Accumulator with no code changes: {handheld_halting.process()}")
    print(f"Accumulator with changes: {handheld_halting.process_with_changes()}")


if __name__ == "__main__":
    print(f"Completed in {timeit.timeit(main, number=1)} seconds")
