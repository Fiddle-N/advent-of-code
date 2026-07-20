from advent_of_code.puzzles.year_2016.day_14 import process


def test_md5_key_search():
    md5_ks = process.MD5KeySearch("abc")
    assert md5_ks.search() == 22728


def test_md5_key_search_with_key_stretching():
    md5_ks = process.MD5KeySearch("abc", key_stretching=True)
    assert md5_ks.search() == 22551
