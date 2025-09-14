import timeit


class ComboBreaker:

    def __init__(self, card_pk: int, door_pk: int):
        self.card_pk = card_pk
        self.door_pk = door_pk
        self.card_loop_size = None
        self.door_loop_size = None
        self.brute_force_loop_size()

    @classmethod
    def from_file(cls):
        with open('input.txt') as f:
            card_pk, door_pk = f.read().splitlines()
            return cls(int(card_pk), int(door_pk))

    def brute_force_loop_size(self):
        self.card_loop_size = self._brute_force_loop_size(self.card_pk)
        self.door_loop_size = self._brute_force_loop_size(self.door_pk)

    @property
    def encryption_key(self):
        card_encryption_key = self._fixed_loop(self.card_pk, self.door_loop_size)
        door_encryption_key = self._fixed_loop(self.door_pk, self.card_loop_size)
        assert card_encryption_key == door_encryption_key
        return card_encryption_key

    @staticmethod
    def _brute_force_loop_size(pk):
        loop_size = 0
        subject_number = 7
        value = 1
        while True:
            loop_size += 1
            value *= subject_number
            value %= 20201227
            if value == pk:
                return loop_size

    def _fixed_loop(self, subject_number, loop_no):
        value = 1
        for loop in range(loop_no):
            value *= subject_number
            value %= 20201227
        return value


def main():
    combo_breaker = ComboBreaker.from_file()
    print('Encryption key:', combo_breaker.encryption_key)


if __name__ == '__main__':
    print(f'Completed in {timeit.timeit(main, number=1)} seconds')
