from typing import Self

from advent_of_code.common import (
    read_file,
    timed_run,
    merge_intervals,
)


class FreshIngredientSolver:
    def __init__(
        self,
        db: list[tuple[int, int]],
        ingredients: list[int],
    ):
        self.db = db
        self.ingredients = ingredients

    @classmethod
    def from_text(cls, raw_input: str) -> Self:
        raw_db, raw_ingredients = raw_input.split("\n\n")
        unmerged_ranges = []
        for raw_range in raw_db.splitlines():
            start, end = raw_range.split("-")
            unmerged_ranges.append((int(start), int(end)))
        merged_ranges = merge_intervals(unmerged_ranges)

        ingredients = [int(i) for i in raw_ingredients.splitlines()]

        return cls(db=merged_ranges, ingredients=ingredients)

    def find_fresh(self):
        fresh = 0
        for i in self.ingredients:
            for fresh_range in self.db:
                if fresh_range[0] <= i <= fresh_range[1]:
                    fresh += 1
                    break
        return fresh

    def total_fresh(self):
        return sum(fresh_range[1] - fresh_range[0] + 1 for fresh_range in self.db)


def run():
    fis = FreshIngredientSolver.from_text(read_file())
    print(fis.find_fresh())
    print(fis.total_fresh())


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
