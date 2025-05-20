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
    you = None
    for o in parse_input(lines):
        if o.name == "YOU":
            you = o
            break
    return find_santa(you, set(), 0)

class Object:
    """object orbit structure definition"""
    def __init__(self, name):
        self.name = name
        self.orbits = set()
        self.orbited_by = set()

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, value):
        return self.name == value

    def orbit_count(self) -> int:
        """return the objects this object orbits"""
        count = len(self.orbits)
        for o in self.orbits:
            count += o.orbit_count()
        return count

def find_santa(obj: Object, path: set, least: int) -> int:
    """recursively search for SAN orbit"""
    if "SAN" in obj.orbits or "SAN" in obj.orbited_by:
        return len(path) - 1
    if 0 < least < len(path) - 1:
        return least
    np = set(path)
    np.add(obj.name)
    for o in obj.orbits | obj.orbited_by:
        if o.name in path:
            continue
        l = find_santa(o, np, least)
        if least == 0 or l < least:
            least = l
    return least

def parse_input(lines: list[str]) -> list[Object]:
    """parse input into objects"""
    objects = {}
    for line in lines:
        o1, o2, *_ = line.split(")")
        obj1 = objects.setdefault(o1, Object(o1))
        obj2 = objects.setdefault(o2, Object(o2))
        obj2.orbits.add(obj1)
        obj1.orbited_by.add(obj2)
    return list(objects.values())

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
sample2 = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN""".splitlines()

# Part 1
assert solve_part1(sample) == 42
assert solve_part1(data) == 150150

# Part 2
assert solve_part2(sample2) == 4
assert solve_part2(data) == 352
