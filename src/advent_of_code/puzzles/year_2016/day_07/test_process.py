import pytest

from advent_of_code.puzzles.year_2016.day_07 import process


@pytest.mark.parametrize(
    "ip, does_support_tls",
    [
        ("abba[mnop]qrst", True),
        ("abcd[bddb]xyyx", False),
        ("aaaa[qwer]tyui", False),
        ("ioxxoj[asdfgh]zxcvbn", True),
    ],
)
def test_supports_tls(ip, does_support_tls) -> None:
    assert process.supports_tls(ip) == does_support_tls


@pytest.mark.parametrize(
    "ip, does_support_ssl",
    [
        ("aba[bab]xyz", True),
        ("xyx[xyx]xyx", False),
        ("aaa[kek]eke", True),
        ("zazbz[bzb]cdb", True),
    ],
)
def test_supports_ssl(ip, does_support_ssl) -> None:
    assert process.supports_ssl(ip) == does_support_ssl
