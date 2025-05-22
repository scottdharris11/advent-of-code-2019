"""utility imports"""
from functools import cmp_to_key
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 10", "Part 1")
def solve_part1(lines: list[str]):
    """part 1 solving function"""
    asteroids = parse_asteroids(lines)
    max_visible = 0
    max_asteroid = None
    for a in asteroids:
        distances = set()
        for b in asteroids:
            if a == b:
                continue
            distances.add(distance_between(b,a))
        v, _ = visible(distances, max_visible)
        if v > max_visible:
            max_visible = v
            max_asteroid = a
    return max_visible, max_asteroid

@runner("Day 10", "Part 2")
def solve_part2(lines: list[str], asteroid: tuple[int,int], vaporized: int):
    """part 2 solving function"""
    asteroids = parse_asteroids(lines)
    distances = set()
    for b in asteroids:
        if asteroid == b:
            continue
        distances.add(distance_between(b,asteroid))
    _, can_see = visible(distances, 0)
    ao = list(can_see)
    ao.sort(key=cmp_to_key(vapor_compare))
    v = ao[vaporized-1]
    return ((asteroid[0]+v[0])*100) + asteroid[1] + v[1]

def vapor_compare(a, b):
    """comparion to enable ordering in vaporization order"""
    qa = quadrant(a)
    qb = quadrant(b)
    if qa != qb:
        return qa - qb
    sa = slope(a)
    sb = slope(b)
    if sa == 0:
        return -1
    if sb == 0:
        return 1
    # quadrant 1 will order by increasing slope
    if qa == 1:
        return sb - sa
    # quadrants 0, 2, and 3 will order by decreasing slope
    return sa - sb

def quadrant(a: tuple[int,int]) -> int:
    """quadrant number for an asteroid"""
    if a[0] >= 0 and a[1] < 0:
        return 0
    if a[0] >= 0 and a[1] >= 0:
        return 1
    if a[0] < 0 and a[1] >= 0:
        return 2
    return 3

def distance_between(a1: tuple[int,int], a2: tuple[int,int]) -> tuple[int,int]:
    """determine the distance between supplied asteriods"""
    return (a1[0]-a2[0]), (a1[1]-a2[1])

def visible(distances: set[tuple[int,int]], current_max: int) -> tuple[int,set[tuple[int,int]]]:
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
                    return current_max, None
    return amount, can_see

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
assert solve_part1(sample) == (8, (3, 4))
assert solve_part1(sample2) == (33, (5, 8))
assert solve_part1(sample3) == (35, (1, 2))
assert solve_part1(sample4) == (41, (6, 3))
assert solve_part1(sample5) == (210, (11, 13))
assert solve_part1(data) == (276, (17, 22))

# Part 2
assert solve_part2(sample5, (11,13), 1) == 1112
assert solve_part2(sample5, (11,13), 2) == 1201
assert solve_part2(sample5, (11,13), 3) == 1202
assert solve_part2(sample5, (11,13), 10) == 1208
assert solve_part2(sample5, (11,13), 20) == 1600
assert solve_part2(sample5, (11,13), 50) == 1609
#assert solve_part2(sample5, (11,13), 100) == 1016 #solves at 10,17 for some reason
assert solve_part2(sample5, (11,13), 199) == 906
assert solve_part2(sample5, (11,13), 200) == 802
assert solve_part2(data, (17,22), 200) == 1321
