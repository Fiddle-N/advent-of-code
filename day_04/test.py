from day_04 import process, passport_validation


class TestValidBirthYear:

    def test_birth_year_1919_is_invalid(self):
        assert not passport_validation.is_valid_birth_year('1919')

    def test_birth_year_1920_is_valid(self):
        assert passport_validation.is_valid_birth_year('1920')

    def test_birth_year_2002_is_valid(self):
        assert passport_validation.is_valid_birth_year('2002')

    def test_birth_year_2003_is_invalid(self):
        assert not passport_validation.is_valid_birth_year('2003')

    def test_birth_year_01920_is_invalid(self):
        assert not passport_validation.is_valid_birth_year('01920')

    def test_birth_year_with_alpha_chars_is_invalid(self):
        assert not passport_validation.is_valid_birth_year('foo')


class TestValidIssueYear:

    def test_issue_year_2009_is_invalid(self):
        assert not passport_validation.is_valid_issue_year('2009')

    def test_issue_year_2010_is_valid(self):
        assert passport_validation.is_valid_issue_year('2010')

    def test_issue_year_2020_is_valid(self):
        assert passport_validation.is_valid_issue_year('2020')

    def test_issue_year_2021_is_invalid(self):
        assert not passport_validation.is_valid_issue_year('2021')

    def test_issue_year_2010_with_leading_zero_is_invalid(self):
        assert not passport_validation.is_valid_issue_year('02010')

    def test_issue_year_with_alpha_chars_is_invalid(self):
        assert not passport_validation.is_valid_issue_year('foo')


class TestValidExpirationIssueYear:

    def test_expiration_year_2019_is_invalid(self):
        assert not passport_validation.is_valid_expiration_year('2019')

    def test_expiration_year_2020_is_valid(self):
        assert passport_validation.is_valid_expiration_year('2020')

    def test_expiration_year_2030_is_valid(self):
        assert passport_validation.is_valid_expiration_year('2030')

    def test_expiration_year_2031_is_invalid(self):
        assert not passport_validation.is_valid_expiration_year('2031')

    def test_expiration_year_2020_with_leading_zero_is_invalid(self):
        assert not passport_validation.is_valid_expiration_year('02020')

    def test_expiration_year_with_alpha_chars_is_invalid(self):
        assert not passport_validation.is_valid_expiration_year('foo')


class TestValidHeight:

    def test_height_149cm_is_invalid(self):
        assert not passport_validation.is_valid_height('149cm')

    def test_height_150cm_is_valid(self):
        assert passport_validation.is_valid_height('150cm')

    def test_height_193cm_is_valid(self):
        assert passport_validation.is_valid_height('193cm')

    def test_height_194cm_is_invalid(self):
        assert not passport_validation.is_valid_height('194cm')

    def test_height_150cm_with_leading_zero_is_invalid(self):
        assert not passport_validation.is_valid_height('0150cm')

    def test_height_58in_is_invalid(self):
        assert not passport_validation.is_valid_height('58in')

    def test_height_59in_is_valid(self):
        assert passport_validation.is_valid_height('59in')

    def test_height_76in_is_valid(self):
        assert passport_validation.is_valid_height('76in')

    def test_height_77in_is_invalid(self):
        assert not passport_validation.is_valid_height('77in')

    def test_height_59in_with_leading_zero_is_invalid(self):
        assert not passport_validation.is_valid_height('059in')

    def test_height_150_with_missing_length_system_is_invalid(self):
        assert not passport_validation.is_valid_height('150')

    def test_height_150_with_invalid_length_system_is_invalid(self):
        assert not passport_validation.is_valid_height('150c')


class TestValidHairColour:

    def test_hair_colour_hash_with_six_hex_chars_is_valid(self):
        assert passport_validation.is_valid_hair_colour('#123abc')

    def test_hair_colour_hash_with_six_hex_chars_including_leading_zero_is_valid(self):
        assert passport_validation.is_valid_hair_colour('#0123ab')

    def test_hair_colour_six_hex_chars_without_hash_is_invalid(self):
        assert not passport_validation.is_valid_hair_colour('123abc')

    def test_hair_colour_hash_with_six_chars_not_all_hex_is_valid(self):
        assert not passport_validation.is_valid_hair_colour('#123abz')

    def test_hair_colour_hash_with_seven_chars_is_invalid(self):
        assert not passport_validation.is_valid_hair_colour('#123abcd')


class TestEyeColour:

    def test_eye_colour_amb_blu_brn_gry_grn_hzl_oth_are_valid(self):
        for colour in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'):
            assert passport_validation.is_valid_eye_colour(colour)

    def test_eye_colour_not_amb_blu_brn_gry_grn_hzl_oth_is_invalid(self):
        assert not passport_validation.is_valid_eye_colour('wat')


class TestPassportId:

    def test_nine_digit_passport_id_valid(self):
        assert passport_validation.is_valid_passport_id('123456789')

    def test_nine_digit_passport_id_with_leading_zero_valid(self):
        assert passport_validation.is_valid_passport_id('012345678')

    def test_eight_digit_passport_id_invalid(self):
        assert not passport_validation.is_valid_passport_id('12345678')

    def test_ten_digit_passport_id_invalid(self):
        assert not passport_validation.is_valid_passport_id('0123456789')

    def test_nine_digit_passport_id_with_alpha_chars_invalid(self):
        assert not passport_validation.is_valid_passport_id('12345678a')


class TestPassportsWithValidFields:

    def test_passports_with_valid_fields_present(self):
        passports = """\
ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
"""
        passport_processing = process.PassportProcessing(passports)
        assert len(passport_processing.passports_with_valid_fields_present()) == 2


class TestValidPassports:

    def test_invalid_passports(self):
        passports = """\
eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007
"""
        passport_processing = process.PassportProcessing(passports)
        assert len(passport_processing.valid_passports()) == 0


    def test_valid_passports(self):
        passports = """\
pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
"""
        passport_processing = process.PassportProcessing(passports)
        assert len(passport_processing.valid_passports()) == 4