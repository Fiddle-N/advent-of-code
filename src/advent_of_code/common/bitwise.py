__all__ = ["int_to_bitstr", "bitstr_to_int", "iter_bits", "ones_mask"]


def int_to_bitstr(int_: int, padding: int = 0) -> str:
    return f"{int_:0{padding}b}"


def bitstr_to_int(bitstr: str) -> int:
    return int(bitstr, 2)


def iter_bits(bitmask: int):
    mask = bitmask
    while mask:
        low_bit = mask & -mask
        yield low_bit
        mask ^= low_bit


def ones_mask(no_of_ones: int) -> int:
    return 2**no_of_ones - 1
