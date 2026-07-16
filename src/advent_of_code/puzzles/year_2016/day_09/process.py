import re
from dataclasses import dataclass
from typing import Literal

from advent_of_code.common import read_file, timed_run

MARKER_PATTERN = r"\((?P<seq_len>\d+)x(?P<repeat>\d+)\)"


@dataclass
class CompressedText:
    repeat: int
    vals: list["str | CompressedText"]

    @property
    def decompressed_length(self) -> int:
        length = 0
        for val in self.vals:
            length += (
                len(val) if isinstance(val, str) else val.decompressed_length
            ) * self.repeat
        return length


class CompressedTextParser:
    def __init__(self, version: Literal[1, 2]):
        self.version = version

    def _parse(self, text: str) -> list[str | CompressedText]:
        output = []
        remaining = text
        while True:
            match_ = re.search(MARKER_PATTERN, remaining)

            if match_ is None:
                # no more markers
                if remaining:
                    output.append(remaining)
                return output

            start = match_.start()
            end = match_.end()
            seq_len = int(match_["seq_len"])
            repeat = int(match_["repeat"])

            left = remaining[:start]
            right = remaining[end:]

            assert len(right) >= seq_len
            seq = right[:seq_len]
            remaining = right[seq_len:]

            if left:
                output.append(left)
            output.append(
                CompressedText(
                    repeat=repeat,
                    vals=(self._parse(seq) if self.version == 2 else [seq]),
                )
            )

    def parse(self, text) -> CompressedText:
        return CompressedText(
            repeat=1,
            vals=self._parse(text),
        )


def run() -> None:
    raw_compressed_text = read_file()
    parser_v1 = CompressedTextParser(version=1)
    compressed_text = parser_v1.parse(raw_compressed_text)
    print(compressed_text.decompressed_length)

    parser_v2 = CompressedTextParser(version=2)
    compressed_text = parser_v2.parse(raw_compressed_text)
    print(compressed_text.decompressed_length)


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
