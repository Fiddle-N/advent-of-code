__all__ = ["int_to_binary", "int_to_hex", "binary_to_int", "iter_bits", "ones_mask"]


def int_to_binary(int_: int, padding: int = 0) -> str:
    return f"{int_:0{padding}b}"


def int_to_hex(int_: int, padding: int = 0) -> str:
    return f"{int_:0{padding}x}"


def binary_to_int(binary: str) -> int:
    return int(binary, 2)


def iter_bits(bitmask: int):
    mask = bitmask
    while mask:
        low_bit = mask & -mask
        yield low_bit
        mask ^= low_bit


def ones_mask(no_of_ones: int) -> int:
    return 2**no_of_ones - 1
