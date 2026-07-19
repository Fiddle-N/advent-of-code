__all__ = ["merge_intervals"]


def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    intervals = sorted(intervals)
    left, right = intervals[:1], intervals[1:]
    for next_i in right:
        last_i = left.pop()
        if last_i[0] <= next_i[0] <= last_i[1]:
            i = (last_i[0], max(last_i[1], next_i[1]))
            left.append(i)
        else:
            left.extend((last_i, next_i))
    return left
