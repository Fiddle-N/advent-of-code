from collections import Counter

from advent_of_code.common import read_file, timed_run


def err_correct(msg: str) -> tuple[str, str]:
    t_msg = zip(*msg.splitlines())
    correct_msg = []
    correct_msg_2 = []
    for chars in t_msg:
        count = Counter(chars)
        most_common = count.most_common()
        correct_msg.append(most_common[0][0])
        correct_msg_2.append(most_common[-1][0])
    return "".join(correct_msg), "".join(correct_msg_2)


def run():
    msg = read_file()
    err_corrected_msgs = err_correct(msg)
    print(err_corrected_msgs[0])
    print(err_corrected_msgs[1])


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
