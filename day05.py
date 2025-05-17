"""utility imports"""
from utilities.data import read_lines, parse_integers
from utilities.runner import runner

@runner("Day 5", "Part 1")
def solve_part1(line: str) -> str:
    """part 1 solving function"""
    opcodes = parse_integers(line, ",")
    return run_program(opcodes, 1)

@runner("Day 5", "Part 2")
def solve_part2(line: str):
    """part 2 solving function"""
    return 0

def run_program(opcodes: list[int], input_val: int) -> str:
    """run the intcode program and return value"""
    output = ""
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
            opcodes[pv(opcodes,i+1,1)] = input_val
            i += 2
        elif opcode == 4:
            dc = pv(opcodes,i+1,m1)
            if dc != 0:
                output += str(dc)
            i += 2
        else:
            print("something broken")
            return None
    return output

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
data = read_lines("input/day05/input.txt")[0]

# Part 1
assert run_program(parse_integers("3,0,4,0,99",","),1) == "1"
assert run_program(parse_integers("1002,4,3,4,33",","),1) == ""
assert solve_part1(data) == "7265618"

# Part 2
assert solve_part2(data) == 0
