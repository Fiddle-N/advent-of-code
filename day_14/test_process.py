from day_14 import process


class TestDecodeVersion1:

    def test_mask_apply_1(self):
        mask = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X'
        input_val = 11
        expected, = process.Version1Decoder.apply_mask(input_val, mask)
        assert expected == 73


    def test_mask_apply_2(self):
        mask = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X'
        input_val = 101
        expected, = process.Version1Decoder.apply_mask(input_val, mask)
        assert expected == 101


    def test_mask_apply_3(self):
        mask = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X'
        input_val = 0
        expected, = process.Version1Decoder.apply_mask(input_val, mask)
        assert expected == 64


    def test_full_program(self):
        init_program = """\
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""
        docking_data = process.Version1Decoder(init_program)
        assert docking_data.run_program() == {7: 101, 8: 64}


class TestDecodeVersion2:

    def test_mask_apply_1(self):
        mask = '000000000000000000000000000000X1001X'
        input_val = 42
        expected = {26, 27, 58, 59}
        actual = set(process.AbstractDecoder.apply_mask(input_val, mask))
        assert expected == actual


    def test_mask_apply_2(self):
        mask = '00000000000000000000000000000000X0XX'
        input_val = 26
        expected = {16, 17, 18, 19, 24, 25, 26, 27}
        actual = set(process.AbstractDecoder.apply_mask(input_val, mask))
        assert expected == actual


    def test_full_program(self):
        init_program = """\
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1"""
        docking_data = process.AbstractDecoder(init_program)
        expected = {
            16: 1,
            17: 1,
            18: 1,
            19: 1,
            24: 1,
            25: 1,
            26: 1,
            27: 1,
            58: 100,
            59: 100,
        }
        actual = docking_data.run_program()
        assert actual == expected
        assert sum(actual.values()) == 208

