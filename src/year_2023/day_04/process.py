import collections
from dataclasses import dataclass
from typing import Any, Self


@dataclass
class Card:
    winning_numbers: set[int]
    your_numbers: set[int]

    @property
    def your_winning_numbers(self) -> set[int]:
        return self.your_numbers & self.winning_numbers


class Scratchcards:

    def __init__(self, scratchcard_input: str) -> None:
        self.cards = {}
        for card in scratchcard_input.splitlines():
            label, numbers = card.split(': ')
            id_ = int(label.split()[1])
            winning_number_seq, your_number_seq = numbers.split('|')
            winning_numbers = set(int(num) for num in winning_number_seq.strip().split())
            your_numbers = set(int(num) for num in your_number_seq.strip().split())
            self.cards[id_] = Card(winning_numbers, your_numbers)

    @classmethod
    def read_file(cls) -> Self:
        with open("input.txt") as f:
            return cls(f.read())

    def points(self) -> dict[int, int]:
        your_points = {}
        for id_, card in self.cards.items():
            card_points = (
                2 ** (len(card.your_winning_numbers) - 1)
                if card.your_winning_numbers
                else 0
            )
            your_points[id_] = card_points
        return your_points

    def total_scratchcards(self) -> dict[int, int]:
        total_scratchcards = collections.Counter()
        last_card_id = max(self.cards)
        for id_, card in self.cards.items():
            # get number of copies for current card
            copies = total_scratchcards[id_]

            # increment value to add original card
            num_of_cards = copies + 1

            # update card data structure with new value
            total_scratchcards[id_] = num_of_cards

            # generate copies of later cards
            won_id = id_
            for _ in card.your_winning_numbers:
                won_id += 1
                if won_id > last_card_id:
                    break
                total_scratchcards[won_id] += num_of_cards

        return total_scratchcards


def sum_dict_values(dict_: dict[Any: int]) -> int:
    return sum(dict_.values())


def main() -> None:
    scratchcards = Scratchcards.read_file()
    print(
        "Sum of scratchcard points:",
        sum_dict_values(scratchcards.points()),
    )
    print(
        "Total scratchcards:",
        sum_dict_values(scratchcards.total_scratchcards()),
    )


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
