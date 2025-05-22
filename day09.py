"""utility imports"""
from utilities.data import read_lines, parse_integers
from utilities.runner import runner

@runner("Day 9", "Part 1")
def solve_part1(line: str, input_val: int):
    """part 1 solving function"""
    computer = Computer(parse_integers(line,","))
    computer.in_signals.append(input_val)
    computer.run()
    return ",".join(map(str,computer.out_signals))

@runner("Day 9", "Part 2")
def solve_part2(line: str):
    """part 2 solving function"""
    return 0

class Computer:
    """structure for computer"""
    def __init__(self, op: list[int]):
        self.op = {i:o for i, o in enumerate(op)}
        self.in_signals = []
        self.out_signals = []
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
                if len(self.in_signals) == 0:
                    break
                self.op[self.pvi(i+1,m1)] = self.in_signals.pop(0)
                i += 2
            elif opcode == 4:
                self.out_signals.append(self.pv(i+1,m1))
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
data = read_lines("input/day09/input.txt")[0]
sample = """109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99""".splitlines()[0]
sample2 = """1102,34915192,34915192,7,4,7,99,0""".splitlines()[0]
sample3 = """104,1125899906842624,99""".splitlines()[0]

# Part 1
assert solve_part1(sample, 0) == "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"
assert solve_part1(sample2, 0) == "1219070632396864"
assert solve_part1(sample3, 0) == "1125899906842624"
assert solve_part1(data, 1) == "4288078517"

# Part 2
assert solve_part2(sample) == 0
assert solve_part2(data) == 0
