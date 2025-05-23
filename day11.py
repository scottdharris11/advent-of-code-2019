"""utility imports"""
from utilities.data import read_lines, parse_integers
from utilities.runner import runner

@runner("Day 11", "Part 1")
def solve_part1(line: str):
    """part 1 solving function"""
    oc = parse_integers(line, ",")
    painter = PaintingRobot()
    computer = Computer(oc, painter)
    computer.run()
    return len(painter.painted_panels)

@runner("Day 11", "Part 2")
def solve_part2(line: str):
    """part 2 solving function"""
    oc = parse_integers(line, ",")
    painter = PaintingRobot()
    painter.painted_panels[painter.location] = 1
    computer = Computer(oc, painter)
    computer.run()

    min_x = None
    max_x = None
    min_y = None
    max_y = None
    for l, c in painter.painted_panels.items():
        if c == 0:
            continue
        x, y = l
        if min_x is None or x < min_x:
            min_x = x
        if max_x is None or x > max_x:
            max_x = x
        if min_y is None or y < min_y:
            min_y = y
        if max_y is None or y > max_y:
            max_y = y

    output_lines = []
    for y in range(min_y,max_y+1):
        row = ""
        for x in range(min_x,max_x+1):
            c = painter.painted_panels.get((x,y), 0)
            if c == 1:
                row += "X"
            else:
                row += " "
        output_lines.append(row)
    return "\n" + "\n".join(output_lines)

UP = (0,-1)
DOWN = (0,1)
RIGHT = (1,0)
LEFT = (-1,0)
TURNS = [UP,RIGHT,DOWN,LEFT]

class PaintingRobot:
    """structure for painting robot"""
    def __init__(self):
        self.painted_panels = {}
        self.location = (0,0)
        self.direction = 0
        self.paint_mode = True

    def provide_input(self) -> int:
        """provide an input value based on the color of panel at current location"""
        return self.painted_panels.get(self.location,0)

    def accept_output(self, o: int):
        """accept output value and perform robot actions accordingly"""
        if self.paint_mode:
            self.painted_panels[self.location] = o
            self.paint_mode = False
        else:
            self.direction += -1 if o == 0 else 1
            if self.direction < 0:
                self.direction = len(TURNS) - 1
            elif self.direction == len(TURNS):
                self.direction = 0
            turn = TURNS[self.direction]
            self.location = (self.location[0]+turn[0], self.location[1]+turn[1])
            self.paint_mode = True

class Computer:
    """structure for computer"""
    def __init__(self, op: list[int], painter: PaintingRobot):
        self.op = {i:o for i, o in enumerate(op)}
        self.painter = painter
        self.opi = 0
        self.relative_base = 0
        self.done = False

    def run(self) -> bool:
        """run the intcode program and return value"""
        i = self.opi
        while i < len(self.op):
            opcode, m1, m2, m3 = self.opcode_modes(self.opc(i))
            if opcode == 99:
                self.done = True
                break
            if opcode == 1:
                self.op[self.pvi(i+3,m3)] = self.pv(i+1,m1) + self.pv(i+2,m2)
                i += 4
            elif opcode == 2:
                self.op[self.pvi(i+3,m3)] = self.pv(i+1,m1) * self.pv(i+2,m2)
                i += 4
            elif opcode == 3:
                self.op[self.pvi(i+1,m1)] = self.painter.provide_input()
                i += 2
            elif opcode == 4:
                self.painter.accept_output(self.pv(i+1,m1))
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

# Data / Test
data = read_lines("input/day11/input.txt")[0]

ptest = PaintingRobot()
ptest.accept_output(1)
ptest.accept_output(0)
assert len(ptest.painted_panels) == 1
ptest.accept_output(0)
ptest.accept_output(0)
assert len(ptest.painted_panels) == 2
ptest.accept_output(1)
ptest.accept_output(0)
assert len(ptest.painted_panels) == 3
ptest.accept_output(1)
ptest.accept_output(0)
assert len(ptest.painted_panels) == 4
ptest.accept_output(0)
ptest.accept_output(1)
assert len(ptest.painted_panels) == 4
ptest.accept_output(1)
ptest.accept_output(0)
assert len(ptest.painted_panels) == 5
ptest.accept_output(1)
ptest.accept_output(0)
assert len(ptest.painted_panels) == 6

# Part 1
assert solve_part1(data) == 2255

# Part 2
assert solve_part2(data) == """
XXX   XX  X  X XXXX XXX   XX  XXX   XX 
X  X X  X X X  X    X  X X  X X  X X  X
XXX  X    XX   XXX  X  X X    X  X X  X
X  X X    X X  X    XXX  X    XXX  XXXX
X  X X  X X X  X    X    X  X X X  X  X
XXX   XX  X  X X    X     XX  X  X X  X"""
