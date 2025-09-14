# @pytest.mark.skip("failing")
# def test_example():
#     text = """COM)B
# B)C
# C)D
# D)E
# E)F
# B)G
# G)H
# D)I
# E)J
# J)K
# K)L
# """
#     orbits, objects, _, _ = process.process_text(text)
#
#     paths = process.find_paths_to_com(orbits, objects)
#     orbit_no = process.calculate_orbits(paths)
#     assert orbit_no == 42
#
#
# @pytest.mark.skip("failing")
# def test_example_2():
#     text = """COM)B
# B)C
# C)D
# D)E
# E)F
# B)G
# G)H
# D)I
# E)J
# J)K
# K)L
# K)YOU
# I)SAN
# """
#     orbits, _, _, _ = process.process_text(text)
#
#     orbit_no = process.len_shortest_path_linear(orbits, "K", "I")
#     assert orbit_no == 4
