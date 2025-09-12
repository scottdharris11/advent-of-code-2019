"""utility imports"""
from utilities.data import read_lines, parse_integers
from utilities.runner import runner

@runner("Day 17", "Part 1")
def solve_part1(line: str) -> int:
    """part 1 solving function"""
    oc = parse_integers(line, ",")
    io = IOProvider()
    computer = Computer(oc, io)
    computer.run()
    grid = Grid(io.scaffold_map.splitlines())
    return alignment_parameters(grid)

@runner("Day 17", "Part 2")
def solve_part2(line: str) -> int:
    """part 2 solving function"""
    return 0

class Grid:
    """strcturue representing the scaffolding grid"""
    def __init__(self, lines: list[str]):
        self.scaffold = set()
        self.intersections = set()
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c == '#':
                    self.scaffold.add((x,y))
        for point in self.scaffold:
            for move in [(0,-1),(1,0),(0,1),(-1,0)]:
                check = (point[0]+move[0],point[1]+move[1])
                if check not in self.scaffold:
                    break
            else:
                self.intersections.add(point)

def alignment_parameters(grid: Grid) -> int:
    """find intersection points and calculate alignment"""
    alignment = 0
    for point in grid.intersections:
        alignment += point[0] * point[1]
    return alignment

class IOProvider:
    """structure for fixing robot"""
    def __init__(self):
        self.scaffold_map = ""

    def provide_input(self):
        """provide input to the program"""
        return 0

    def accept_output(self, o: int):
        """accept output value and record mapping actions accordingly"""
        self.scaffold_map += chr(o)

    def halt_program(self) -> bool:
        """exit point to stop program"""
        return False

class Computer:
    """structure for computer"""
    def __init__(self, op: list[int], io: IOProvider):
        self.op = {i:o for i, o in enumerate(op)}
        self.io = io
        self.opi = 0
        self.relative_base = 0
        self.done = False

    def run(self) -> bool:
        """run the intcode program and return value"""
        i = self.opi
        while i < len(self.op):
            opcode, m1, m2, m3 = self.opcode_modes(self.opc(i))
            if opcode == 99 or self.io.halt_program():
                self.done = True
                break
            if opcode == 1:
                self.op[self.pvi(i+3,m3)] = self.pv(i+1,m1) + self.pv(i+2,m2)
                i += 4
            elif opcode == 2:
                self.op[self.pvi(i+3,m3)] = self.pv(i+1,m1) * self.pv(i+2,m2)
                i += 4
            elif opcode == 3:
                self.op[self.pvi(i+1,m1)] = self.io.provide_input()
                i += 2
            elif opcode == 4:
                self.io.accept_output(self.pv(i+1,m1))
                i += 2
            elif opcode == 5:
                if self.pv(i+1,m1) != 0:
                    i = self.pv(i+2,m2)
                else:
                    i += 3
            elif opcode == 6:
                if self.pv(i+1,m1) == 0:
                    i = self.pv(i+2,m2)
                else:
                    i += 3
            elif opcode == 7:
                self.op[self.pvi(i+3,m3)] = 1 if self.pv(i+1,m1) < self.pv(i+2,m2) else 0
                i += 4
            elif opcode == 8:
                self.op[self.pvi(i+3,m3)] = 1 if self.pv(i+1,m1) == self.pv(i+2,m2) else 0
                i += 4
            elif opcode == 9:
                self.relative_base += self.pv(i+1,m1)
                i += 2
        self.opi = i

    def opc(self, i: int) -> int:
        """get the value of supplied index"""
        return self.op.get(i, 0)

    def opcode_modes(self, o: int) -> tuple[int,int,int,int]:
        """parse opcode and modes from input"""
        mode3 = 0
        if o > 20000:
            mode3 = 2
            o -= 20000
        elif o > 10000:
            mode3 = 1
            o -= 10000
        mode2 = 0
        if o > 2000:
            mode2 = 2
            o -= 2000
        elif o > 1000:
            mode2 = 1
            o -= 1000
        mode1 = 0
        if o > 200:
            mode1 = 2
            o -= 200
        elif o > 100:
            mode1 = 1
            o -= 100
        return o, mode1, mode2, mode3

    def pv(self, idx: int, mode: int) -> int:
        """determine proper param value based on index and mode"""
        if mode == 0:
            return self.opc(self.opc(idx))
        if mode == 1:
            return self.opc(idx)
        return self.opc(self.opc(idx) + self.relative_base)

    def pvi(self, idx: int, mode: int) -> int:
        """determine proper param value index based on index and mode"""
        if mode in [0,1]:
            return self.opc(idx)
        return self.opc(idx) + self.relative_base

# Data
data = read_lines("input/day17/input.txt")[0]
sample = """..#..........
..#..........
#######...###
#.#...#...#.#
#############
..#...#...#..
..#####...^..""".splitlines()

# Part 1
assert alignment_parameters(Grid(sample)) == 76
assert solve_part1(data) == 4688

# Part 2
assert solve_part2(data) == 0
