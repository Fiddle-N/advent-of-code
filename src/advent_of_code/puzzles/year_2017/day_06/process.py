from operator import itemgetter

from advent_of_code.common import read_file, timed_run


def parse_memory(raw_mem: str) -> list[int]:
    return [int(mem_bank) for mem_bank in raw_mem.split()]


def redistribute(memory: list[int]) -> tuple[list[int], int]:
    memory = memory.copy()
    seen = set()
    cycle = 0
    while True:
        curr_memory = tuple(memory)
        if curr_memory in seen:
            return memory, cycle
        seen.add(curr_memory)

        cycle += 1

        max_bank, max_blocks = max(enumerate(memory), key=itemgetter(1))
        base_block_redist, excess_banks = divmod(max_blocks, len(memory))

        memory[max_bank] = 0

        starting_bank = max_bank + 1
        for excess_bank_val, bank_idx in enumerate(
            range(starting_bank, starting_bank + len(memory))
        ):
            block_redist = (
                base_block_redist + 1
                if excess_bank_val < excess_banks
                else base_block_redist
            )
            memory[bank_idx % len(memory)] += block_redist


def run():
    raw_memory = read_file()
    memory = parse_memory(raw_memory)
    seen_memory, cycles = redistribute(memory)
    print(cycles)
    _, max_cycles = redistribute(seen_memory)
    print(max_cycles)


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
