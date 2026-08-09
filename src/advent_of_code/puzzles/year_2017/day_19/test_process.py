from advent_of_code.puzzles.year_2017.day_19 import process


def test_traverse() -> None:
    raw_route = """\
     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+ """
    route = process.parse(raw_route)
    assert process.RouteTraverser(route).traverse() == ("ABCDEF", 38)
