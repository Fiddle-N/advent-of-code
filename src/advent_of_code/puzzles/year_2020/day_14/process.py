import itertools
import re
import timeit


class AbstractDecoder:
    def __init__(self, program=None):
        program = program if program is not None else self._read_file()
        self.program = program.splitlines()
        self.mask_length = len(self._process_mask(self.program[0]))
        self.mask_regex = r"mem\[(?P<location>\d+)] = (?P<value>\d+)"

    @staticmethod
    def _process_mask(line):
        _, mask = line.split(" = ")
        return mask

    @staticmethod
    def _read_file():
        with open("input.txt") as f:
            return f.read()

    @staticmethod
    def apply_bit_mask(bit_input, mask):
        """Takes in a bit input and mask and returns a bit output"""
        raise NotImplementedError

    @classmethod
    def apply_mask(cls, input_val, mask):
        bit_input = f"{input_val:036b}"
        outputs = cls.apply_bit_mask(bit_input, mask)
        dec_outputs = ["".join(output) for output in outputs]
        mem_outputs = [int(output, base=2) for output in dec_outputs]
        return mem_outputs

    def process_mem(self, line, mask):
        """Takes in an input line and mask and returns memory address and the corresponding memory value"""
        raise NotImplementedError

    def run_program(self):
        current_mask = None
        memory = {}
        for line in self.program:
            if line.startswith("mask"):
                mask = self._process_mask(line)
                assert len(mask) == self.mask_length
                current_mask = mask
            elif line.startswith("mem"):
                mem_locations, mem_value = self.process_mem(line, current_mask)
                for mem_location in mem_locations:
                    memory[mem_location] = mem_value
            else:
                raise Exception
        return memory


class Version1Decoder(AbstractDecoder):
    @classmethod
    def apply_bit_mask(cls, bit_input, mask):
        output = []
        for input_char, mask_char in zip(bit_input, mask):
            if mask_char == "X":
                output_char = input_char
            else:
                output_char = mask_char
            output.append(output_char)
        return [output]

    def process_mem(self, line, mask):
        if (mem_re := re.fullmatch(self.mask_regex, line)) is not None:
            locations = [int(mem_re.group("location"))]
            raw_value = int(mem_re.group("value"))
            (value,) = self.apply_mask(raw_value, mask)
            return locations, value


class Version2Decoder(AbstractDecoder):
    @classmethod
    def apply_bit_mask(cls, bit_input, mask):
        product_input = []
        for input_char, mask_char in zip(bit_input, mask):
            if mask_char == "0":
                choice = input_char
            elif mask_char == "1":
                choice = mask_char
            elif mask_char == "X":
                choice = "01"
            else:
                raise Exception
            product_input.append(choice)
        return itertools.product(*product_input)

    def process_mem(self, line, mask):
        if (mem_re := re.fullmatch(self.mask_regex, line)) is not None:
            raw_location = int(mem_re.group("location"))
            value = int(mem_re.group("value"))
            locations = self.apply_mask(raw_location, mask)
            return locations, value


def main():
    v1_decoder = Version1Decoder()
    result_v1 = v1_decoder.run_program()
    print(f"Version 1 Decoder Chip Result: {sum(result_v1.values())}")
    v2_decoder = Version2Decoder()
    result_v2 = v2_decoder.run_program()
    print(f"Version 2 Decoder Chip Result: {sum(result_v2.values())}")


if __name__ == "__main__":
    print(f"Completed in {timeit.timeit(main, number=1)} seconds")
