# Solutions

When attempting to solve a problem but the solution will either be far too complex or slow, consider the following:

1. Consider if you are using the right data structure. For example: 
   1. If doing many "in" checks, consider using a set (O(1)) rather than a list (O(n)).
   2. If needing to access both ends of a sequence, consider using a deque (O(1) to remove the left side) rather than a
   list (O(n) to remove the left side).
   3. If needing to concat many strings, instead of adding the strings (worst case O(n^2) if adding a char one at a
   time), consider using a list (O(1) append) and then joining at the end.
   4. If there is the possibility of recomputing values, especially in heavy recursive algorithms, then consider using
   a cache (explicit or with using @functools.cache).
   5. If needing to do many copies of a list or dict, consider if bitsets can be used (e.g. for BFS/Dijkstra).
2. Consider if there may be periodicity to the problem input. Do you recompute any inputs multiple times? If so, you 
   may only need to perform computations for a specific cycle.
3. If a Part 2 question, check to see if there are any pointers in Part 1 that may help.
4. If there are simply lots of calculations to make, then think about optimisations to cut down the number of
   computations.
   1. The classic example of this - is the real input set up differently from the example input such that you can choose
   a vastly more simplified/performant algorithm? Often, test inputs are red herrings; or meant to be illustrative of 
   some trick that you would need to understand the real algorithm to solve the puzzle.
