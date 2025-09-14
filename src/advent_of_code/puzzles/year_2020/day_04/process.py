import timeit

import passport_validation


class PassportProcessing:

    passport_field_validation = {
        "byr": passport_validation.is_valid_birth_year,
        "iyr": passport_validation.is_valid_issue_year,
        "eyr": passport_validation.is_valid_expiration_year,
        "hgt": passport_validation.is_valid_height,
        "hcl": passport_validation.is_valid_hair_colour,
        "ecl": passport_validation.is_valid_eye_colour,
        "pid": passport_validation.is_valid_passport_id,
    }

    def __init__(self, passport_data=None):
        passport_data = passport_data if passport_data is not None else self.read_file()
        self.passports = self.preprocess(passport_data)

    @staticmethod
    def read_file():
        with open("input.txt") as f:
            return f.read().strip()

    @staticmethod
    def preprocess(data):
        passports = []
        passport_groups = data.split("\n\n")
        for passport_group in passport_groups:
            passport = {}
            for passport_line in passport_group.split("\n"):
                for passport_key_value in passport_line.strip().split():
                    key, value = passport_key_value.split(":")
                    passport[key] = value
            passports.append(passport)
        return passports

    def is_valid_fields_present(self, passport):
        passport_keys = set(passport.keys())
        required_keys = set(self.passport_field_validation)
        return required_keys.issubset(passport_keys)

    def passports_with_valid_fields_present(self):
        passports_with_valid_fields_present = [
            passport
            for passport in self.passports
            if self.is_valid_fields_present(passport)
        ]
        return passports_with_valid_fields_present

    def is_valid_passport(self, passport):
        for field, validation_fn in self.passport_field_validation.items():
            is_valid_field = validation_fn(passport[field])
            if not is_valid_field:
                return False
        return True

    def valid_passports(self):
        passports_with_valid_fields_present = self.passports_with_valid_fields_present()
        valid_passports = [
            passport
            for passport in passports_with_valid_fields_present
            if self.is_valid_passport(passport)
        ]
        return valid_passports


def main():
    passport_processing = PassportProcessing()
    print(
        f"Passports with valid fields present: {len(passport_processing.passports_with_valid_fields_present())}"
    )
    print(f"Valid passports: {len(passport_processing.valid_passports())}")


if __name__ == "__main__":
    print(f"Completed in {timeit.timeit(main, number=1)} seconds")
