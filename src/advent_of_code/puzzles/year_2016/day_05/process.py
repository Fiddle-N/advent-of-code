from itertools import count
from hashlib import md5
from typing import cast

from tqdm import tqdm

from advent_of_code.common import (
    read_file,
    timed_run,
)


PASSWORD_LENGTH = 8


def generate_pw_door_1(door_id: str) -> str:
    pw = ""
    for i in count():
        hash_input = door_id + str(i)
        hasher = md5()
        hasher.update(hash_input.encode("utf-8"))
        hex_ = hasher.hexdigest()
        if hex_[:5] == "00000":
            pw += hex_[5]
        if len(pw) == PASSWORD_LENGTH:
            return pw
    raise Exception("This code is unreachable")


def generate_pw_door_2(door_id: str, cinematic_animation: bool = False) -> str:
    if cinematic_animation:
        pbar = tqdm(
            total=PASSWORD_LENGTH, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}"
        )

    pw: list[str | None] = [None] * PASSWORD_LENGTH
    for i in count():
        hash_input = door_id + str(i)
        hasher = md5()
        hasher.update(hash_input.encode("utf-8"))
        hex_ = hasher.hexdigest()
        if hex_[:5] != "00000":
            continue
        try:
            pos = int(hex_[5])
        except ValueError:
            # 6th char is a letter
            continue
        if not 0 <= pos <= 7:
            continue
        if pw[pos] is not None:
            continue
        pw[pos] = hex_[6]

        if cinematic_animation:
            pbar.set_description(f"DECRYPTING: Processed position {pos}")
            pbar.update(1)

        if all(letter is not None for letter in pw):
            completed_pw = cast(list[str], pw)
            if cinematic_animation:
                pbar.close()
            return "".join(completed_pw)

    raise Exception("This code is unreachable")


def run():
    door_id = read_file()
    print(generate_pw_door_1(door_id))
    print(generate_pw_door_2(door_id, cinematic_animation=True))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
