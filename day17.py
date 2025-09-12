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
    return grid.alignment_parameters()

@runner("Day 17", "Part 2")
def solve_part2(line: str) -> int:
    """part 2 solving function"""
    oc = parse_integers(line, ",")
    io = IOProvider()
    computer = Computer(oc, io)
    computer.run()
    grid = Grid(io.scaffold_map.splitlines())
    path = grid.cleaner_path()

    # for now, i manually can see the splits, haven't figured out
    # a way to achieve via code
    #print(path)
    func_a = "R,8,L,6,L,4,L,10,R,8"
    func_b = "L,4,R,4,L,4,R,8"
    func_c = "L,6,L,4,R,8"
    main = path.replace(func_a, "A").replace(func_b, "B").replace(func_c, "C")

    # setup and run intcode computer
    io.input_instructions = to_ascii_code("\n".join([main,func_a,func_b,func_c,'n']))
    io.input_instructions.append(10)
    io.collecting = True
    oc[0] = 2
    computer = Computer(oc, io)
    computer.run()
    return io.dust_collected

MOVES = ['^','>','v','<']
ADJUST = [(0,-1), (1,0), (0,1), (-1,0)]

class Grid:
    """strcturue representing the scaffolding grid"""
    def __init__(self, lines: list[str]):
        self.scaffold = set()
        self.intersections = set()
        self.cleaner = None
        self.cleaner_dir = None
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c == '#':
                    self.scaffold.add((x,y))
                elif c in MOVES:
                    self.scaffold.add((x,y))
                    self.cleaner = (x,y)
                    self.cleaner_dir = MOVES.index(c)
        for point in self.scaffold:
            for move in [(0,-1),(1,0),(0,1),(-1,0)]:
                check = (point[0]+move[0],point[1]+move[1])
                if check not in self.scaffold:
                    break
            else:
                self.intersections.add(point)

    def alignment_parameters(self) -> int:
        """find intersection points and calculate alignment"""
        alignment = 0
        for point in self.intersections:
            alignment += point[0] * point[1]
        return alignment

    def cleaner_path(self) -> str:
        """build path for cleaner to visit all scaffolding locations"""
        path = ""
        moving = ADJUST[self.cleaner_dir]
        loc = self.cleaner
        visited = set()
        visited.add(loc)
        steps = 0
        while visited != self.scaffold:
            nloc = (loc[0]+moving[0],loc[1]+moving[1])
            if nloc not in self.scaffold:
                # keeping it simple here as it seems as if from viewing 
                # the grid that you can visit all spaces by following a
                # path that only turns left or right at end of
                # straightaway without need to backtrace.
                for t, c in [(-1,'L'),(1,'R')]:
                    nmove = turn(moving, t)
                    nloc = (loc[0]+nmove[0],loc[1]+nmove[1])
                    if nloc in self.scaffold:
                        if steps != 0:
                            path += str(steps) + ","
                        steps = 0
                        path += c + ","
                        moving = nmove
                        break
            else:
                visited.add(nloc)
                loc = nloc
                steps += 1
        path += str(steps)
        return path

def turn(moving: tuple[int,int], t: int) -> tuple[int,int]:
    """adjust the current moving based on a left or right turn"""
    ci = ADJUST.index(moving)
    ci += t
    if ci < 0:
        ci = len(ADJUST) - 1
    if ci == len(ADJUST):
        ci = 0
    return ADJUST[ci]

def to_ascii_code(instructions: str) -> list[int]:
    """convert ascii input instructions into intcodes"""
    output = []
    for i in instructions:
        output.append(ord(i))
    return output

class IOProvider:
    """structure for fixing robot"""
    def __init__(self):
        self.scaffold_map = ""
        self.collecting = False
        self.input_instructions = []
        self.input_idx = 0
        self.dust_collected = None

    def provide_input(self):
        """provide input to the program"""
        instruct = self.input_instructions[self.input_idx]
        self.input_idx += 1
        return instruct

    def accept_output(self, o: int):
        """accept output value and record mapping actions accordingly"""
        if self.collecting:
            self.dust_collected = o
        else:
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
sample = Grid("""..#..........
..#..........
#######...###
#.#...#...#.#
#############
..#...#...#..
..#####...^..""".splitlines())

# Part 1
assert sample.alignment_parameters() == 76
assert solve_part1(data) == 4688

# Part 2
assert solve_part2(data) == 714866
