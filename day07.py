"""utility imports"""
from utilities.data import read_lines, parse_integers
from utilities.runner import runner

@runner("Day 7", "Part 1")
def solve_part1(line: str):
    """part 1 solving function"""
    opcodes = parse_integers(line, ",")
    sequences = set()
    phase_sequences(4, 5, tuple(), sequences)
    max_output = 0
    for seq in sequences:
        value = 0
        for phase in seq:
            value = run_program(list(opcodes), phase, value)
        if value > max_output:
            max_output = value
    return max_output

@runner("Day 7", "Part 2")
def solve_part2(line: str):
    """part 2 solving function"""
    return 0

def phase_sequences(max_phase: int, to_assign: int, values: tuple, sequences: set):
    """build unique sequences"""
    if to_assign == 0:
        sequences.add(values)
        return
    for p in range(max_phase+1):
        if p in values:
            continue
        v = list(values)
        v.append(p)
        phase_sequences(max_phase, to_assign-1, tuple(v), sequences)

def run_program(opcodes: list[int], phase: int, input_val: int) -> str:
    """run the intcode program and return value"""
    phase_entered = False
    i = 0
    while i < len(opcodes):
        opcode, m1, m2, _ = opcode_modes(opcodes[i])
        if opcode == 99:
            break
        if opcode == 1:
            opcodes[pv(opcodes,i+3,1)] = pv(opcodes,i+1,m1) + pv(opcodes,i+2,m2)
            i += 4
        elif opcode == 2:
            opcodes[pv(opcodes,i+3,1)] = pv(opcodes,i+1,m1) * pv(opcodes,i+2,m2)
            i += 4
        elif opcode == 3:
            if phase_entered:
                opcodes[pv(opcodes,i+1,1)] = input_val
            else:
                opcodes[pv(opcodes,i+1,1)] = phase
                phase_entered = True
            i += 2
        elif opcode == 4:
            dc = pv(opcodes,i+1,m1)
            return dc
        elif opcode == 5:
            if pv(opcodes,i+1,m1) != 0:
                i = pv(opcodes,i+2,m2)
            else:
                i += 3
        elif opcode == 6:
            if pv(opcodes,i+1,m1) == 0:
                i = pv(opcodes,i+2,m2)
            else:
                i += 3
        elif opcode == 7:
            opcodes[pv(opcodes,i+3,1)] = 1 if pv(opcodes,i+1,m1) < pv(opcodes,i+2,m2) else 0
            i += 4
        elif opcode == 8:
            opcodes[pv(opcodes,i+3,1)] = 1 if pv(opcodes,i+1,m1) == pv(opcodes,i+2,m2) else 0
            i += 4
        else:
            print("something broken")
            return None
    return 0

def opcode_modes(o: int) -> tuple[int,int,int,int]:
    """parse opcode and modes from input"""
    mode3 = 0
    if o > 10000:
        mode3 = 1
        o -= 10000
    mode2 = 0
    if o > 1000:
        mode2 = 1
        o -= 1000
    mode1 = 0
    if o > 100:
        mode1 = 1
        o -= 100
    return o, mode1, mode2, mode3

def pv(opcodes: list[int], idx: int, mode: int) -> int:
    """determine proper param value based on index and mode"""
    return opcodes[opcodes[idx]] if mode == 0 else opcodes[idx]

# Data
data = read_lines("input/day07/input.txt")[0]
sample = """3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0""".splitlines()[0]
sample2 = """3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0""".splitlines()[0]
sample3 = """3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,03,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0""".splitlines()[0]

# Part 1
assert solve_part1(sample) == 43210
assert solve_part1(sample2) == 54321
assert solve_part1(sample3) == 65210
assert solve_part1(data) == 255590

# Part 2
assert solve_part2(sample) == 0
assert solve_part2(data) == 0
