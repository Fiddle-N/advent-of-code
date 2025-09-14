import unittest
from advent_of_code.puzzles.year_2019.day_01 import process


class TestTotalFuel(unittest.TestCase):
    def test_2_initial_fuel_returns_2(self):
        self.assertEqual(process.total_fuel(2), 2)

    def test_654_initial_fuel_returns_966(self):
        self.assertEqual(process.total_fuel(654), 966)

    def test_33583_initial_fuel_returns_50346(self):
        self.assertEqual(process.total_fuel(33583), 50346)


if __name__ == "__main__":
    unittest.main()
