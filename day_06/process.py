import timeit


class CustomCustoms:

    def __init__(self, form_data=None):
        form_data = form_data if form_data is not None else self._read_file()
        self.forms = self._preprocess(form_data)

    @staticmethod
    def _read_file():
        with open('input.txt') as f:
            return f.read().strip()

    @staticmethod
    def _preprocess(form_data):
        form_groups = form_data.split('\n\n')
        forms = [form_answers.splitlines() for form_answers in form_groups]
        return forms

    def questions_answered(self, mode):
        set_operations = {'anyone': set.union, 'everyone': set.intersection}
        questions_anyone_answered = 0
        for form_group in self.forms:
            form_group_set = (set(form) for form in form_group)
            form_answers = set_operations[mode](*form_group_set)
            questions_anyone_answered += len(form_answers)
        return questions_anyone_answered


def main():
    custom_customs = CustomCustoms()
    print(f"Questions anyone answered: {custom_customs.questions_answered('anyone')}")
    print(f"Questions everyone answered: {custom_customs.questions_answered('everyone')}")


if __name__ == '__main__':
    print(f'Completed in {timeit.timeit(main, number=1)} seconds')
