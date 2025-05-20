"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 6", "Part 1")
def solve_part1(lines: list[str]):
    """part 1 solving function"""
    objects = parse_input(lines)
    orbits = 0
    for o in objects:
        orbits += o.orbit_count()
    return orbits

@runner("Day 6", "Part 2")
def solve_part2(lines: list[str]):
    """part 2 solving function"""
    return 0

class Object:
    """object orbit structure definition"""
    def __init__(self, name):
        self.name = name
        self.orbits = []

    def __repr__(self):
        return self.name

    def orbit_count(self) -> int:
        """return the objects this object orbits"""
        count = len(self.orbits)
        for o in self.orbits:
            count += o.orbit_count()
        return count

def parse_input(lines: list[str]) -> list[Object]:
    """parse input into objects"""
    objects = {}
    for line in lines:
        o1, o2, *_ = line.split(")")
        obj1 = objects.setdefault(o1, Object(o1))
        obj2 = objects.setdefault(o2, Object(o2))
        obj2.orbits.append(obj1)
    return objects.values()

# Data
data = read_lines("input/day06/input.txt")
sample = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L""".splitlines()

# Part 1
assert solve_part1(sample) == 42
assert solve_part1(data) == 150150

# Part 2
assert solve_part2(sample) == 0
assert solve_part2(data) == 0
