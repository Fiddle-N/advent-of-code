import pytest

from year_2023.day_15 import process


def test_hash():
    assert process.hash_('HASH') == 52


def test_hash_with_init_seq():
    init_seq = 'rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'.split(',')
    hashed_init_seq = [process.hash_(step) for step in init_seq]
    assert hashed_init_seq == [30, 253, 97, 47, 14, 180, 9, 197, 48, 214, 231]
    assert sum(hashed_init_seq) == 1320


def test_len_install():
    init_seq = 'rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'.split(',')
    lens_install = process.LensInstall(init_seq)
    lens_install_iter = iter(lens_install)

    exp_results = [
        {
            0: {
                'first_label': 'rn',
                'last_label': 'rn',
                'box': {
                    'rn': process.BoxLens(focal_length=1, prev=None, next_=None),
                },
            },
        },
        {
            0: {
                'first_label': 'rn',
                'last_label': 'rn',
                'box': {
                    'rn': process.BoxLens(focal_length=1, prev=None, next_=None),
                },
            },
        },
        {
            0: {
                'first_label': 'rn',
                'last_label': 'rn',
                'box': {
                    'rn': process.BoxLens(focal_length=1, prev=None, next_=None),
                },
            },
            1: {
                'first_label': 'qp',
                'last_label': 'qp',
                'box': {
                    'qp': process.BoxLens(focal_length=3, prev=None, next_=None),
                },
            },
        },
        {
            0: {
                'first_label': 'rn',
                'last_label': 'cm',
                'box': {
                    'rn': process.BoxLens(focal_length=1, prev=None, next_='cm'),
                    'cm': process.BoxLens(focal_length=2, prev='rn', next_=None),
                },
            },
            1: {
                'first_label': 'qp',
                'last_label': 'qp',
                'box': {
                    'qp': process.BoxLens(focal_length=3, prev=None, next_=None),
                },
            },
        },
        {
            0: {
                'first_label': 'rn',
                'last_label': 'cm',
                'box': {
                    'rn': process.BoxLens(focal_length=1, prev=None, next_='cm'),
                    'cm': process.BoxLens(focal_length=2, prev='rn', next_=None),
                },
            },
            1: {
                'first_label': None,
                'last_label': None,
                'box': {},
            },
        },
        {
            0: {
                'first_label': 'rn',
                'last_label': 'cm',
                'box': {
                    'rn': process.BoxLens(focal_length=1, prev=None, next_='cm'),
                    'cm': process.BoxLens(focal_length=2, prev='rn', next_=None),
                },
            },
            1: {
                'first_label': None,
                'last_label': None,
                'box': {},
            },
            3: {
                'first_label': 'pc',
                'last_label': 'pc',
                'box': {
                    'pc': process.BoxLens(focal_length=4, prev=None, next_=None),
                },
            },
        },
        {
            0: {
                'first_label': 'rn',
                'last_label': 'cm',
                'box': {
                    'rn': process.BoxLens(focal_length=1, prev=None, next_='cm'),
                    'cm': process.BoxLens(focal_length=2, prev='rn', next_=None),
                },
            },
            1: {
                'first_label': None,
                'last_label': None,
                'box': {},
            },
            3: {
                'first_label': 'pc',
                'last_label': 'ot',
                'box': {
                    'pc': process.BoxLens(focal_length=4, prev=None, next_='ot'),
                    'ot': process.BoxLens(focal_length=9, prev='pc', next_=None),
                },
            },
        },
        {
            0: {
                'first_label': 'rn',
                'last_label': 'cm',
                'box': {
                    'rn': process.BoxLens(focal_length=1, prev=None, next_='cm'),
                    'cm': process.BoxLens(focal_length=2, prev='rn', next_=None),
                },
            },
            1: {
                'first_label': None,
                'last_label': None,
                'box': {},
            },
            3: {
                'first_label': 'pc',
                'last_label': 'ab',
                'box': {
                    'pc': process.BoxLens(focal_length=4, prev=None, next_='ot'),
                    'ot': process.BoxLens(focal_length=9, prev='pc', next_='ab'),
                    'ab': process.BoxLens(focal_length=5, prev='ot', next_=None),
                },
            },
        },
        {
            0: {
                'first_label': 'rn',
                'last_label': 'cm',
                'box': {
                    'rn': process.BoxLens(focal_length=1, prev=None, next_='cm'),
                    'cm': process.BoxLens(focal_length=2, prev='rn', next_=None),
                },
            },
            1: {
                'first_label': None,
                'last_label': None,
                'box': {},
            },
            3: {
                'first_label': 'ot',
                'last_label': 'ab',
                'box': {
                    'ot': process.BoxLens(focal_length=9, prev=None, next_='ab'),
                    'ab': process.BoxLens(focal_length=5, prev='ot', next_=None),
                },
            },
        },
        {
            0: {
                'first_label': 'rn',
                'last_label': 'cm',
                'box': {
                    'rn': process.BoxLens(focal_length=1, prev=None, next_='cm'),
                    'cm': process.BoxLens(focal_length=2, prev='rn', next_=None),
                },
            },
            1: {
                'first_label': None,
                'last_label': None,
                'box': {},
            },
            3: {
                'first_label': 'ot',
                'last_label': 'pc',
                'box': {
                    'ot': process.BoxLens(focal_length=9, prev=None, next_='ab'),
                    'ab': process.BoxLens(focal_length=5, prev='ot', next_='pc'),
                    'pc': process.BoxLens(focal_length=6, prev='ab', next_=None),
                },
            },
        },
        {
            0: {
                'first_label': 'rn',
                'last_label': 'cm',
                'box': {
                    'rn': process.BoxLens(focal_length=1, prev=None, next_='cm'),
                    'cm': process.BoxLens(focal_length=2, prev='rn', next_=None),
                },
            },
            1: {
                'first_label': None,
                'last_label': None,
                'box': {},
            },
            3: {
                'first_label': 'ot',
                'last_label': 'pc',
                'box': {
                    'ot': process.BoxLens(focal_length=7, prev=None, next_='ab'),
                    'ab': process.BoxLens(focal_length=5, prev='ot', next_='pc'),
                    'pc': process.BoxLens(focal_length=6, prev='ab', next_=None),
                },
            },
        },
    ]

    for exp_result, result in zip(exp_results, lens_install_iter):
        assert len(exp_result) == len(result)
        for exp_box_no, exp_box_details in exp_result.items():
            box_details = result[exp_box_no]
            for attr, val in exp_box_details.items():
                assert getattr(box_details, attr) == val

    with pytest.raises(StopIteration):
        next(lens_install_iter)

    focusing_power = process.focusing_power(result)
    assert focusing_power == {
        'rn': 1,
        'cm': 4,
        'ot': 28,
        'ab': 40,
        'pc': 72,
    }
    assert sum(focusing_power.values()) == 145
