"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 24", "Part 1")
def solve_part1(lines: list[str]):
    """part 1 solving function"""
    bugs = parse_input(lines, False)
    previous = set()
    previous.add(frozenset(bugs))
    while True:
        bugs = next_bug_state(bugs)
        state = frozenset(bugs)
        if state in previous:
            break
        previous.add(state)
    return biodiversity(bugs)

@runner("Day 24", "Part 2")
def solve_part2(lines: list[str], minutes: int):
    """part 2 solving function"""
    bugs = parse_input(lines, True)
    min_depth = 0
    max_depth = 0
    for m in range(minutes):
        bugs, min_depth, max_depth = rnext_bug_state(bugs, min_depth, max_depth)
        print(f"after minute {m+1}: min_depth = {min_depth}, max_depth = {max_depth}")
        for d in range(min_depth, max_depth+1):
            print(f"Depth {d}")
            for y in range(5):
                line = ""
                for x in range(5):
                    if (d,x,y) in bugs:
                        line += '#'
                    else:
                        line += '.'
                print(line)
            print("")
    return len(bugs)

def biodiversity(bugs: set[tuple[int,int]]) -> int:
    """calcluate the biodiversity of the bug state"""
    rating = 0
    for y in range(5):
        for x in range(5):
            if (x,y) in bugs:
                p = (y * 5) + x
                rating += pow(2, p)
    return rating

def next_bug_state(bugs: set[tuple[int,int,int]]) -> set[tuple[int,int]]:
    """determine next bug state from current"""
    nbugs = set()
    for y in range(5):
        for x in range(5):
            adjancent = 0
            for moves in [(0,-1),(1,0),(0,1),(-1,0)]:
                ax = x + moves[0]
                ay = y + moves[1]
                if ax < 0 or ay < 0 or ax == 5 or ay == 5:
                    continue
                if (ax,ay) in bugs:
                    adjancent += 1
            if (x,y) in bugs:
                if adjancent == 1:
                    nbugs.add((x,y))
            else:
                if adjancent in [1,2]:
                    nbugs.add((x,y))
    return nbugs

RMOVES = {
    (0,0): [(-1,2,1),(0,1,0),(0,0,1),(-1,1,2)], #1!
    (1,0): [(-1,2,1),(0,2,0),(0,1,1),(0,0,0)], #2!
    (2,0): [(-1,2,1),(0,3,0),(0,2,1),(0,1,0)], #3!
    (3,0): [(-1,2,1),(0,4,0),(0,3,1),(0,2,0)], #4!
    (4,0): [(-1,2,1),(-1,3,2),(0,4,1),(0,3,0)], #5!

    (0,1): [(0,0,0),(0,1,1),(0,0,2),(-1,1,2)], #6!
    (1,1): [(0,1,0),(0,2,1),(0,1,3),(0,0,1)], #7!
    (2,1): [(0,2,0),(0,3,1),(1,0,0),(1,1,0),(1,2,0),(1,3,0),(1,4,0),(0,1,1)], #8!
    (3,1): [(0,3,0),(0,4,1),(0,3,2),(0,2,1)], #9!
    (4,1): [(0,4,0),(-1,3,2),(0,4,2),(0,3,1)], #10!

    (0,2): [(0,0,1),(0,1,2),(0,0,3),(-1,1,2)], #11!
    (1,2): [(0,1,1),(1,0,0),(1,0,1),(1,0,2),(1,0,3),(1,0,4),(0,1,3),(0,0,2)], #12!
    (2,2): None, #? (Middle: portal to next depth)
    (3,2): [(0,3,1),(0,4,2),(0,3,3),(1,4,0),(1,4,1),(1,4,2),(1,4,3),(1,4,4)], #14!
    (4,2): [(0,4,1),(-1,3,2),(0,4,3),(0,3,2)], #15!

    (0,3): [(0,0,2),(0,1,3),(0,0,4),(-1,1,2)], #16!
    (1,3): [(0,1,2),(0,2,3),(0,1,4),(0,0,3)], #17!
    (2,3): [(1,0,4),(1,1,4),(1,2,4),(1,3,4),(1,4,4),(0,3,3),(0,2,4),(0,1,3)], #18!
    (3,3): [(0,3,2),(0,4,3),(0,3,4),(0,2,3)], #19!
    (4,3): [(0,4,2),(-1,3,2),(0,4,4),(0,3,3)],  #20!

    (0,4): [(0,0,3),(0,1,4),(-1,2,3),(-1,1,2)], #21!
    (1,4): [(0,1,3),(0,2,4),(-1,2,3),(0,0,4)], #22!
    (2,4): [(0,2,3),(0,3,4),(-1,2,3),(0,1,4)], #23!
    (3,4): [(0,3,3),(0,4,4),(-1,2,3),(0,2,4)], #24!
    (4,4): [(0,4,3),(-1,3,2),(-1,2,3),(0,3,4)], #25!
}

def rnext_bug_state(bugs: set[tuple[int,int,int]], min_depth: int, max_depth: int):
    """determine next bug state from current"""
    nbugs = set()
    nmin_depth = min_depth
    nmax_depth = max_depth
    for d in range(min_depth-1, max_depth+2):
        for y in range(5):
            for x in range(5):
                if y == 2 and x == 2:
                    continue
                adjancent = 0
                for moves in RMOVES[(x,y)]:
                    ad = d + moves[0]
                    ax = moves[1]
                    ay = moves[2]
                    if (ad,ax,ay) in bugs:
                        adjancent += 1
                if (d,x,y) in bugs:
                    if adjancent == 1:
                        nbugs.add((d,x,y))
                        nmin_depth = min(d,nmin_depth)
                        nmax_depth = max(d,nmax_depth)
                else:
                    if 0 < adjancent < 3:
                        nbugs.add((d,x,y))
                        nmin_depth = min(d,nmin_depth)
                        nmax_depth = max(d,nmax_depth)
    return nbugs, nmin_depth, nmax_depth

def parse_input(lines: list[str], recursive: bool) -> set[tuple[int,int,int]]:
    """parse input for problem"""
    bugs = set()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == '#':
                if recursive:
                    bugs.add((0,x,y))
                else:
                    bugs.add((x,y))
    return bugs

# Data
data = read_lines("input/day24/input.txt")
sample = """....#
#..#.
#..##
..#..
#....""".splitlines()

# Part 1
assert solve_part1(sample) == 2129920
assert solve_part1(data) == 18371095

# Part 2
assert solve_part2(sample, 10) == 99
assert solve_part2(data, 200) == 0
