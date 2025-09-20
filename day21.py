"""utility imports"""
from utilities.data import read_lines, parse_integers
from utilities.runner import runner

@runner("Day 21", "Part 1")
def solve_part1(line: str) -> int:
    """part 1 solving function"""
    oc = parse_integers(line, ",")
    script = [
        "NOT B J", # two steps a way is pit with landing after #..#.
        "AND D J",
        "NOT A T", # next step a pit .
        "OR T J",
        "NOT C T", # three steps away is pit with landing after ##.#
        "AND D T",
        "OR T J",
        "WALK"
    ]
    io = IOProvider(to_ascii_code(script))
    computer = Computer(oc, io)
    computer.run()
    if io.output_vals[-1] > 255:
        return io.output_vals[-1]
    print(to_ascii(io.output_vals))
    return -1

@runner("Day 21", "Part 2")
def solve_part2(line: str) -> int:
    """part 2 solving function"""
    oc = parse_integers(line, ",")
    script = [
        "NOT B J", # two steps a way is pit with landing after #..#.
        "AND D J",
        "NOT C T", # three steps away is pit with landing after ##.#
        "AND D T",
        "AND H T", # exclude scenarios where eight away is not landing ##.#.#
        "OR T J",
        "NOT A T", # next step a pit .
        "OR T J",
        "RUN"
    ]
    io = IOProvider(to_ascii_code(script))
    computer = Computer(oc, io)
    computer.run()
    if io.output_vals[-1] > 255:
        return io.output_vals[-1]
    print(to_ascii(io.output_vals))
    return -1

def to_ascii_code(lines: list[str]) -> list[int]:
    """convert ascii input instructions into intcodes"""
    output = []
    for line in lines:
        for i in line:
            output.append(ord(i))
        output.append(10)
    return output

def to_ascii(vals: list[int]) -> str:
    """convert output intcodes to string"""
    output = ""
    for val in vals:
        if val > 255:
            continue
        output += chr(val)
    return output

class IOProvider:
    """structure for robot"""
    def __init__(self, instructions: list[int]):
        self.instructions = instructions
        self.instructions_idx = 0
        self.output_vals = []

    def provide_input(self):
        """provide input to the program"""
        instruct = self.instructions[self.instructions_idx]
        self.instructions_idx += 1
        return instruct

    def accept_output(self, o: int):
        """accept output value and record mapping actions accordingly"""
        self.output_vals.append(o)

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
data = read_lines("input/day21/input.txt")[0]

# Part 1
assert solve_part1(data) == 19354928

# Part 2
assert solve_part2(data) == 1141997803
