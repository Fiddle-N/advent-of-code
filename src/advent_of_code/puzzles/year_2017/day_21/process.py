from itertools import batched

from advent_of_code.common import read_file, timed_run


type Square = tuple[tuple[str, ...], ...]

START: Square = (
    (".", "#", "."),
    (".", ".", "#"),
    ("#", "#", "#"),
)


def _parse_square(raw_square: str) -> Square:
    return tuple(tuple(row) for row in raw_square.split("/"))


def _rotate(square: Square) -> Square:
    # rotates clockwise
    return tuple(zip(*reversed(square)))


def _flip(square: Square) -> Square:
    return tuple(tuple(reversed(row)) for row in square)


def parse(raw_transformations: str) -> dict[Square, Square]:
    transformations = {}
    for raw_transformation in raw_transformations.splitlines():
        raw_source, raw_target = raw_transformation.split(" => ")
        source = _parse_square(raw_source)
        target = _parse_square(raw_target)
        transformations[source] = target
        transformations[_flip(source)] = target
        for _ in range(3):
            source = _rotate(source)
            transformations[source] = target
            transformations[_flip(source)] = target
    return transformations


def _chunk(square: Square, n: int) -> list[list[Square]]:
    chunks = []
    for batched_rows in batched(square, n, strict=True):
        chunked_row = []
        rows_t = zip(*batched_rows)
        for chunk_t in batched(rows_t, n, strict=True):
            chunk = tuple(zip(*chunk_t))
            chunked_row.append(chunk)
        chunks.append(chunked_row)
    return chunks


def _combine(chunks: list[list[Square]]) -> Square:
    square = []
    for chunk_row in chunks:
        rows_t = []
        for chunk in chunk_row:
            chunk_t = list(zip(*chunk))
            rows_t.extend(chunk_t)
        rows = list(zip(*rows_t))
        square.extend(rows)
    return tuple(square)


def _enhance(square: Square, transformations: dict[Square, Square]) -> Square:
    if len(square) % 2 == 0:
        chunks = _chunk(square, n=2)
    else:
        assert len(square) % 3 == 0
        chunks = _chunk(square, n=3)
    transformed_chunks = [[transformations[chunk] for chunk in row] for row in chunks]
    combined = _combine(transformed_chunks)
    return combined


def enhance(
    transformations: dict[Square, Square], n: int, start: Square = START
) -> Square:
    square = start
    for _ in range(n):
        square = _enhance(square, transformations)
    return square


def count_on_pixels(square: Square) -> int:
    return sum(sum([px == "#" for px in row]) for row in square)


def run():
    raw_transformations = read_file()
    transformations = parse(raw_transformations)
    result = enhance(transformations, n=5)
    print(count_on_pixels(result))
    result = enhance(transformations, n=(18 - 5), start=result)
    print(count_on_pixels(result))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
