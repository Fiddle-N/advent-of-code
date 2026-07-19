__all__ = ["read_file"]


def read_file() -> str:
    with open("input.txt") as f:
        return f.read().rstrip("\n")
