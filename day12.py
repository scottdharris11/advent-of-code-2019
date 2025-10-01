"""utility imports"""
import math
import re
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 12", "Part 1")
def solve_part1(lines: list[str], steps: int) -> int:
    """part 1 solving function"""
    moons = parse_moons(lines)
    for _ in range(steps):
        total_energy = 0
        g = [moon.gravity_impact(moons) for moon in moons]
        for i, moon in enumerate(moons):
            moon.apply_gravity(g[i])
            moon.apply_velocity()
            total_energy += moon.energy()
    return total_energy

@runner("Day 12", "Part 2")
def solve_part2(lines: list[str]) -> int:
    """part 2 solving function"""
    moons = parse_moons(lines)
    orig_state = [[moon.axis_state(axis) for axis in range(3)] for moon in moons]
    # track and record the individual cycles of each moon/axis until
    # we have found all of them
    cycles = [[None, None, None] for _ in range(len(moons))]
    candidates = [[[],[],[]] for _ in range(len(moons))]
    steps = 0
    done = False
    while not done:
        steps += 1
        g = [moon.gravity_impact(moons) for moon in moons]
        done = True
        for i, moon in enumerate(moons):
            moon.apply_gravity(g[i])
            moon.apply_velocity()
            for axis in range(3):
                if cycles[i][axis] is None:
                    equal = moon.axis_state(axis) == orig_state[i][axis]
                    c = track_cycle(steps, equal, candidates[i][axis])
                    if c is not None:
                        cycles[i][axis] = c
                    else:
                        done = False
    # once we have all cycle, determine the least common multiple of
    # each of the cycle values to determine the overall step at which
    # the universe will repeat
    cycle_steps = {s for c in cycles for s in c}
    return math.lcm(*cycle_steps)

def track_cycle(steps: int, equal: bool, candidates: list[int]) -> int:
    """track and verify cycle values"""
    cycle_match = False
    for c in list(candidates):
        if steps % c == 0:
            cycle_match = True
            if equal:
                # verified cycle, use as the cycle value for this point
                return c
            # not equal, means, while it did match at one point,
            # this step count is not representing a cycle
            candidates.remove(c)
    if equal and not cycle_match:
        candidates.append(steps)
    return None

class Moon:
    """moon structure"""
    def __init__(self, position: tuple[int,int,int]):
        self.position = position
        self.velocity = (0,0,0)

    def __repr__(self):
        return str(self.state())

    def state(self) -> tuple[tuple[int,int,int],tuple[int,int,int]]:
        """state of the moon"""
        return (self.position, self.velocity)

    def axis_state(self, axis: int) -> tuple[int,int]:
        """axis state of the moon"""
        return (self.position[axis], self.velocity[axis])

    def gravity_impact(self, moons: list) -> tuple[int,int,int]:
        """calculate current gravitational impact"""
        gx, gy, gz = 0, 0, 0
        x, y, z = self.position
        for moon in moons:
            mx, my, mz = moon.position
            if mx != x:
                gx += 1 if mx > x else -1
            if my != y:
                gy += 1 if my > y else -1
            if mz != z:
                gz += 1 if mz > z else -1
        return gx, gy, gz

    def apply_gravity(self, g: tuple[int,int,int]):
        """apply the gravitational impact"""
        vx, vy, vz = self.velocity
        gx, gy, gz = g
        self.velocity = (vx+gx, vy+gy, vz+gz)

    def apply_velocity(self):
        """apply the current velocity to position"""
        x, y, z = self.position
        vx, vy, vz = self.velocity
        self.position = (x+vx, y+vy, z+vz)

    def energy(self):
        """calculate the energy of the moon"""
        pe = sum(abs(i) for i in self.position)
        ke = sum(abs(i) for i in self.velocity)
        return pe * ke

def parse_moons(lines: list[str]) -> list[Moon]:
    """parse moons from input"""
    moons = []
    mp = re.compile(r"<x=([-\d]+), y=([-\d]+), z=([-\d]+)>")
    for line in lines:
        m = mp.match(line)
        pos = (int(m.group(1)), int(m.group(2)), int(m.group(3)))
        moons.append(Moon(pos))
    return moons

# Data
data = read_lines("input/day12/input.txt")
sample = """<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>""".splitlines()
sample2 = """<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>""".splitlines()

# Part 1
assert solve_part1(sample, 10) == 179
assert solve_part1(sample2, 100) == 1940
assert solve_part1(data, 1000) == 9139

# Part 2
assert solve_part2(sample) == 2772
assert solve_part2(sample2) == 4686774924
assert solve_part2(data) == 420788524631496
