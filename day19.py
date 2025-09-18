"""utility imports"""
from utilities.data import read_lines, parse_integers
from utilities.runner import runner

@runner("Day 19", "Part 1")
def solve_part1(line: str, grid_size: int) -> int:
    """part 1 solving function"""
    oc = parse_integers(line, ",")
    impact_points = 0
    for y in range(grid_size):
        for x in range(grid_size):
            if in_beam(oc, x, y):
                impact_points += 1
    return impact_points

@runner("Day 19", "Part 2")
def solve_part2(line: str) -> int:
    """part 2 solving function"""
    oc = parse_integers(line, ",")
    x, y = 500, 1000 # educated guess based on looking at beam early path
    prev_match = None
    while True:
        tl, tr, bl = fits_ship(oc, x, y)
        #print(f"x/y: ({x},{y}), top_left: {tl}, top_right: {tr}, bottom_left: {bl}")
        if tl and tr and bl:
            if prev_match == (x,y):
                break
            prev_match = (x,y)
            x -= 1
            y -= 1
        if not tl:
            x += 1
            y += 1
        if not bl:
            x += 1
        if not tr:
            y += 1
    return (x * 10000) + y

def fits_ship(oc: list[int], x: int, y: int) -> tuple[bool,bool,bool]:
    """determine if the ship will fit in tractor beam at supplied coords"""
    tl = in_beam(oc, x, y)
    tr = in_beam(oc, x+99, y)
    bl = in_beam(oc, x, y+99)
    return (tl,tr,bl)

def in_beam(oc: list[int], x: int, y: int) -> bool:
    """determines if point is within the beam"""
    io = IOProvider()
    io.coords = [x, y]
    computer = Computer(oc, io)
    computer.run()
    return io.output_val == 1

class IOProvider:
    """structure for fixing robot"""
    def __init__(self):
        self.coord_idx = 0
        self.coords = []
        self.output_val = None

    def provide_input(self):
        """provide input to the program"""
        coord = self.coords[self.coord_idx]
        self.coord_idx += 1
        return coord

    def accept_output(self, o: int):
        """accept output value and record mapping actions accordingly"""
        self.output_val = o

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
data = read_lines("input/day19/input.txt")[0]

# Part 1
assert solve_part1(data, 50) == 158

# Part 2
assert solve_part2(data) == 6191165
