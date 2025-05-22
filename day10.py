"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 10", "Part 1")
def solve_part1(lines: list[str]):
    """part 1 solving function"""
    asteroids = parse_asteroids(lines)
    max_see = 0
    for a in asteroids:
        distances = set()
        for b in asteroids:
            if a == b:
                continue
            distances.add(distance_between(b,a))
        max_see = visible(distances, max_see)
    return max_see

@runner("Day 10", "Part 2")
def solve_part2(lines: list[str]):
    """part 2 solving function"""
    return 0

def distance_between(a1: tuple[int,int], a2: tuple[int,int]) -> tuple[int,int]:
    """determine the distance between supplied asteriods"""
    return (a1[0]-a2[0]), (a1[1]-a2[1])

def visible(distances: set[tuple[int,int]], current_max: int) -> int:
    """count the visible asteroids"""
    can_see = set(distances)
    amount = len(can_see)
    for d1 in distances:
        if d1 not in can_see:
            continue
        d1_dist = total_distance(d1)
        d1_slope = slope(d1)
        for d2 in distances:
            if d1 == d2 or d2 not in can_see:
                continue
            blocked = False
            if d1[0] == 0 and d2[0] == 0 and closer(d1[1], d2[1]):
                blocked = True
            elif d1[1] == 0 and d2[1] == 0 and closer(d1[0], d2[0]):
                blocked = True
            elif d1[0] == 0 or d1[1] == 0 or d2[0] == 0 or d2[1] == 0:
                blocked = False
            elif not same_side(d1[0],d2[0]) or not same_side(d1[1],d2[1]):
                blocked = False
            elif d1_slope == slope(d2) and d1_dist < total_distance(d2):
                blocked = True
            if blocked:
                can_see.remove(d2)
                amount -= 1
                if amount <= current_max:
                    return current_max
    return amount

def same_side(a, b) -> bool:
    """determine if points are on the same side of zero"""
    return a < 0 > b or a > 0 < b

def slope(t) -> float:
    """calculate the slope based on difference"""
    return 0 if t[1] == 0 or t[0] == 0 else t[1] / t[0]

def closer(a, b) -> bool:
    """determine if a is closer to zero than b"""
    return b < a < 0 or b > a > 0

def total_distance(t) -> int:
    """calculate the total distance based on difference"""
    return abs(t[1]) + abs(t[0])

def parse_asteroids(lines: list[str]) -> set[tuple[int,int]]:
    """parse asteroid locations from input"""
    asteroids = set()
    for y, row in enumerate(lines):
        for x, col in enumerate(row):
            if col == '#':
                asteroids.add((x,y))
    return asteroids

# Data
data = read_lines("input/day10/input.txt")
sample = """.#..#
.....
#####
....#
...##""".splitlines()
sample2 = """......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####""".splitlines()
sample3 = """#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.""".splitlines()
sample4 = """.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..""".splitlines()
sample5 = """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##""".splitlines()

# Part 1
assert solve_part1(sample) == 8
assert solve_part1(sample2) == 33
assert solve_part1(sample3) == 35
assert solve_part1(sample4) == 41
assert solve_part1(sample5) == 210
assert solve_part1(data) == 276

# Part 2
assert solve_part2(sample) == 0
assert solve_part2(data) == 0
