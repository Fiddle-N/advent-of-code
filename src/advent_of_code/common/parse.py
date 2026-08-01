def parse_ints(raw: str) -> list[int]:
    return [int(num) for num in raw.splitlines()]
