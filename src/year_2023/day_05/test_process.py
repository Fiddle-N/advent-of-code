from year_2023.day_05 import process


def test_resolve_individual_seeds():
    almanac_input = """\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""

    almanac = process.Almanac(almanac_input)
    seed_details = process.resolve_individual_seed_details(almanac)
    assert seed_details == [
        process.SeedDetail(
            seed=79, soil=81, fertilizer=81, water=81, light=74, temperature=78, humidity=78, location=82
        ),
        process.SeedDetail(
            seed=14, soil=14, fertilizer=53, water=49, light=42, temperature=42, humidity=43, location=43
        ),
        process.SeedDetail(
            seed=55, soil=57, fertilizer=57, water=53, light=46, temperature=82, humidity=82, location=86
        ),
        process.SeedDetail(
            seed=13, soil=13, fertilizer=52, water=41, light=34, temperature=34, humidity=35, location=35
        ),
    ]
    assert process.min_individual_seed_locations(seed_details) == 35


def test_resolve_seed_ranges():
    input_ = """\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""

    almanac = process.Almanac(input_)
    seed_range_details = process.resolve_seed_range_details(almanac)
    assert seed_range_details == [
        process.SeedRangeDetail(
            seed={process.CategoryRange(start=79, range_=14)},
            soil={process.CategoryRange(start=81, range_=14)},
            fertilizer={process.CategoryRange(start=81, range_=14)},
            water={process.CategoryRange(start=81, range_=14)},
            light={process.CategoryRange(start=74, range_=14)},
            temperature={
                process.CategoryRange(start=45, range_=11),
                process.CategoryRange(start=78, range_=3)
            },
            humidity={
                process.CategoryRange(start=46, range_=11),
                process.CategoryRange(start=78, range_=3)
            },
            location={
                process.CategoryRange(start=46, range_=10),
                process.CategoryRange(start=60, range_=1),
                process.CategoryRange(start=82, range_=3)
            },
        ),
        process.SeedRangeDetail(
            seed={process.CategoryRange(start=55, range_=13)},
            soil={process.CategoryRange(start=57, range_=13)},
            fertilizer={process.CategoryRange(start=57, range_=13)},
            water={
                process.CategoryRange(start=53, range_=4),
                process.CategoryRange(start=61, range_=9)
            },
            light={
                process.CategoryRange(start=46, range_=4),
                process.CategoryRange(start=54, range_=9)
            },
            temperature={
                process.CategoryRange(start=82, range_=4),
                process.CategoryRange(start=90, range_=9)
            },
            humidity={
                process.CategoryRange(start=82, range_=4),
                process.CategoryRange(start=90, range_=9)
            },
            location={
                process.CategoryRange(start=86, range_=4),
                process.CategoryRange(start=94, range_=3),
                process.CategoryRange(start=56, range_=4),
                process.CategoryRange(start=97, range_=2),
            },
        ),
    ]
    assert process.min_seed_range_locations(seed_range_details) == 46
