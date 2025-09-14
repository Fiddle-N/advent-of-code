import collections
import timeit


class BinaryBoarding:
    def __init__(self, rows, cols):
        self.seats = []
        with open("input.txt") as f:
            for boarding_pass in f:
                seat = self.process_pass(boarding_pass.rstrip())
                self.seats.append(seat)
        self.rows = rows
        self.cols = cols

    @staticmethod
    def _process_pass(seat_str, lower_letter, upper_letter):
        binary_pass = seat_str.replace(lower_letter, "0").replace(upper_letter, "1")
        return int(binary_pass, base=2)

    @staticmethod
    def process_pass(boarding_pass):
        row_str, col_str = boarding_pass[:7], boarding_pass[7:]
        row = BinaryBoarding._process_pass(row_str, lower_letter="F", upper_letter="B")
        col = BinaryBoarding._process_pass(col_str, lower_letter="L", upper_letter="R")
        return row, col

    @staticmethod
    def get_seat_id(seat):
        row, col = seat
        return row * 8 + col

    def highest_seat_id(self):
        highest_seat_id = 0
        for seat in self.seats:
            seat_id = self.get_seat_id(seat)
            if seat_id > highest_seat_id:
                highest_seat_id = seat_id
        return highest_seat_id

    def find_my_seat(self):
        seats_by_row = collections.defaultdict(list)
        for seat_row, seat_col in self.seats:
            seats_by_row[seat_row].append(seat_col)
        incomplete_rows = {
            row: cols for row, cols in seats_by_row.items() if len(cols) != self.cols
        }
        very_front = min(incomplete_rows)
        very_back = max(incomplete_rows)
        my_row = {
            row: cols
            for row, cols in incomplete_rows.items()
            if row not in (very_front, very_back)
        }
        (my_seat_row,) = list(my_row.keys())
        (potential_seat_cols,) = list(my_row.values())
        (my_seat_col,) = set(range(self.cols)) - set(potential_seat_cols)
        return my_seat_row, my_seat_col


def main():
    binary_boarding = BinaryBoarding(rows=120, cols=8)
    print(f"Highest seat id = {binary_boarding.highest_seat_id()}")
    print(f"My seat id = {binary_boarding.get_seat_id(binary_boarding.find_my_seat())}")


if __name__ == "__main__":
    print(f"Completed in {timeit.timeit(main, number=1)} seconds")
