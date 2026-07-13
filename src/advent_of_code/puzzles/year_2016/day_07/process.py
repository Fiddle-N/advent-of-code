import re
from more_itertools import windowed
from typing import cast

from advent_of_code.common import read_file, timed_run


def _split_ip(ip: str) -> tuple[list[str], list[str]]:
    non_hnet = []
    hnet = []
    for idx, split_ in enumerate(re.split(r"\W+", ip)):
        if not split_:
            continue
        if idx % 2 == 0:
            non_hnet.append(split_)
        else:
            hnet.append(split_)
    return non_hnet, hnet


def _contains_abba(section: str) -> bool:
    if len(section) < 4:
        return False
    for chunk in windowed(section, 4):
        if (chunk[0] != chunk[1]) and (chunk[:2] == chunk[4:1:-1]):
            return True
    return False


def _get_xyx(section: str) -> set[str]:
    if len(section) < 3:
        return set()
    xyxs = set()
    for chunk in windowed(section, 3):
        verified_chunk = cast(tuple[str, str, str], chunk)
        if (verified_chunk[0] != verified_chunk[1]) and (
            verified_chunk[0] == verified_chunk[2]
        ):
            xyxs.add("".join(verified_chunk))
    return xyxs


def _flip_xyx(xyx: str) -> str:
    # assumes xyx already checked
    return xyx[1] + xyx[0] + xyx[1]


def supports_tls(ip: str) -> bool:
    snet, hnet = _split_ip(ip)
    return any(_contains_abba(section) for section in snet) and all(
        not _contains_abba(section) for section in hnet
    )


def supports_ssl(ip: str) -> bool:
    snet, hnet = _split_ip(ip)
    snet_aba = set.union(*(_get_xyx(section) for section in snet))
    hnet_bab = set.union(*(_get_xyx(section) for section in hnet))
    snet_bab = {_flip_xyx(aba) for aba in snet_aba}
    return bool(snet_bab & hnet_bab)


def run():
    ips = read_file().splitlines()
    print(sum(supports_tls(ip) for ip in ips))
    print(sum(supports_ssl(ip) for ip in ips))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
