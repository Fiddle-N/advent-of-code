import itertools
from dataclasses import dataclass
from typing import Self

import parse


@dataclass(frozen=True)
class Map:
    dest_start: int
    source_start: int
    range_: int

    @property
    def dest_end(self):
        return self.dest_start + self.range_ - 1

    @property
    def source_end(self):
        return self.source_start + self.range_ - 1

    @property
    def source_to_dest_overlap(self):
        return self.dest_start - self.source_start


@dataclass(frozen=True)
class SeedDetail:
    seed: int
    soil: int
    fertilizer: int
    water: int
    light: int
    temperature: int
    humidity: int
    location: int


@dataclass(frozen=True)
class CategoryRange:
    start: int
    range_: int

    @property
    def end(self):
        return self.start + self.range_ - 1


@dataclass(frozen=True)
class SeedRangeDetail:
    seed: set[CategoryRange]
    soil: set[CategoryRange]
    fertilizer: set[CategoryRange]
    water: set[CategoryRange]
    light: set[CategoryRange]
    temperature: set[CategoryRange]
    humidity: set[CategoryRange]
    location: set[CategoryRange]


class Almanac:

    def __init__(self, almanac_input):
        seed_input, *maps_input = almanac_input.split('\n\n')
        seed_label, seeds = seed_input.split(': ')
        self.seeds = [int(seed) for seed in seeds.strip().split()]

        self.category_map = {}
        self.maps = {}
        for map_ in maps_input:
            map_label, *map_nums = map_.split('\n')

            parsed_label = parse.parse('{source_category}-to-{dest_category} map:', map_label)
            source_category = parsed_label['source_category']
            dest_category = parsed_label['dest_category']
            self.category_map[source_category] = dest_category

            self.maps[(source_category, dest_category)] = [
                Map(*[int(num) for num in nums.split()])
                for nums in map_nums
            ]

    @classmethod
    def read_file(cls) -> Self:
        with open("input.txt") as f:
            return cls(f.read().strip())


def _calculate_dest_val(category_map, source_val):
    for map_ in category_map:
        if map_.source_start <= source_val < (map_.source_start + map_.range_):
            offset = source_val - map_.source_start
            dest_val = map_.dest_start + offset
            return dest_val
    # if no dest val can be calculated, use source val as this value instead
    return source_val


def resolve_individual_seed_details(almanac):
    all_seed_details = []
    for seed in almanac.seeds:
        source_category = 'seed'
        source_category_val = seed
        seed_details = {source_category: source_category_val}

        while dest_category := almanac.category_map.get(source_category):
            maps = almanac.maps[(source_category, dest_category)]

            dest_category_val = _calculate_dest_val(maps, source_category_val)

            seed_details[dest_category] = dest_category_val

            source_category = dest_category
            source_category_val = dest_category_val

        all_seed_details.append(SeedDetail(**seed_details))

    return all_seed_details


def min_individual_seed_locations(seed_details):
    return min([seed_detail.location for seed_detail in seed_details])


def _calculate_dest_ranges(category_map, source_ranges):
    dest_ranges = set()

    ranges_before_map = source_ranges

    for map_line in category_map:
        ranges_after_map = []
        for range_ in ranges_before_map:
            is_overlap = (range_.start <= map_line.source_end) and (map_line.source_start <= range_.end)

            if not is_overlap:
                # if no overlap found, carry range over to the next map range
                ranges_after_map.append(range_)
                continue

            # overlap found
            # calculate overlap
            overlap = (
                max(range_.start, map_line.source_start),
                min(range_.end, map_line.source_end)
            )

            # convert overlap to dest range in start-end format
            dest_overlap = tuple(
                val + map_line.source_to_dest_overlap
                for val in overlap
            )

            # convert dest range to start + range format
            dest_range = CategoryRange(start=dest_overlap[0], range_=dest_overlap[1] - dest_overlap[0] + 1)

            dest_ranges.add(dest_range)

            # calculate values left over on either side of overlap to try with next map range
            leftover_ranges_start_end = []

            if range_.start < overlap[0]:
                leftover_ranges_start_end.append((range_.start, overlap[0] - 1))

            if range_.end > overlap[1]:
                leftover_ranges_start_end.append((overlap[1] + 1, range_.end))

            leftover_ranges = [
                CategoryRange(start=start, range_=end - start + 1)
                for start, end in leftover_ranges_start_end
            ]

            ranges_after_map.extend(leftover_ranges)

        # all leftover ranges are tried with the next map ranges
        ranges_before_map = ranges_after_map

    # if leftover ranges remains after all maps, include as-is with the current destination ranges
    dest_ranges.update(ranges_before_map)

    return dest_ranges


def resolve_seed_range_details(almanac):
    # generate seed range pairs
    seed_ranges = [
        CategoryRange(*list(pair))
        for pair in itertools.batched(almanac.seeds, 2)
    ]

    seed_range_details = []

    for seed_range in seed_ranges:
        source_category = 'seed'
        source_category_ranges = {seed_range}
        seed_details = {source_category: source_category_ranges}

        while dest_category := almanac.category_map.get(source_category):
            maps = almanac.maps[(source_category, dest_category)]

            dest_category_ranges = _calculate_dest_ranges(maps, source_category_ranges)

            seed_details[dest_category] = dest_category_ranges

            source_category = dest_category
            source_category_ranges = dest_category_ranges

        seed_range_details.append(SeedRangeDetail(**seed_details))

    return seed_range_details


def min_seed_range_locations(seed_range_details):
    return min(
        [
            location.start
            for seed_range_detail in seed_range_details
            for location in seed_range_detail.location
        ]
    )


def main() -> None:
    almanac = Almanac.read_file()
    print(
        "Lowest location number for any initial seed:",
        min_individual_seed_locations(resolve_individual_seed_details(almanac)),
    )
    print(
        "Lowest location number for any initial seed with seed ranges:",
        min_seed_range_locations(resolve_seed_range_details(almanac)),
    )


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
