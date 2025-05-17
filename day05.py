"""utility imports"""
from utilities.data import read_lines, parse_integers
from utilities.runner import runner

@runner("Day 5", "Part 1")
def solve_part1(line: str, input_val: int) -> str:
    """part 1 solving function"""
    opcodes = parse_integers(line, ",")
    return run_program(opcodes, input_val)

@runner("Day 5", "Part 2")
def solve_part2(line: str, input_val: int):
    """part 2 solving function"""
    opcodes = parse_integers(line, ",")
    return run_program(opcodes, input_val)

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
assert solve_part1("3,0,4,0,99", 1) == "1"
assert solve_part1("1002,4,3,4,33", 1) == ""
assert solve_part1(data, 1) == "7265618"

# Part 2
assert solve_part2("3,9,8,9,10,9,4,9,99,-1,8",8) == "1"
assert solve_part2("3,9,8,9,10,9,4,9,99,-1,8",7) == ""
assert solve_part2("3,9,7,9,10,9,4,9,99,-1,8",7) == "1"
assert solve_part2("3,9,7,9,10,9,4,9,99,-1,8",8) == ""
assert solve_part2("3,9,7,9,10,9,4,9,99,-1,8",9) == ""
assert solve_part2("3,3,1108,-1,8,3,4,3,99",8) == "1"
assert solve_part2("3,3,1108,-1,8,3,4,3,99",9) == ""
assert solve_part2("3,3,1107,-1,8,3,4,3,99",5) == "1"
assert solve_part2("3,3,1107,-1,8,3,4,3,99",8) == ""
assert solve_part2("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9",0) == ""
assert solve_part2("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9",1) == "1"
assert solve_part2("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9",5) == "1"
assert solve_part2("3,3,1105,-1,9,1101,0,0,12,4,12,99,1",0) == ""
assert solve_part2("3,3,1105,-1,9,1101,0,0,12,4,12,99,1",2) == "1"
assert solve_part2("3,3,1105,-1,9,1101,0,0,12,4,12,99,1",3) == "1"
assert solve_part2("3,21,1008,21,8,20,1005,20,22,107,8,21,20,"+
                   "1006,20,31,1106,0,36,98,0,0,1002,21,125,20,"+
                   "4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,"+
                   "20,4,20,1105,1,46,98,99",7) == "999"
assert solve_part2("3,21,1008,21,8,20,1005,20,22,107,8,21,20,"+
                   "1006,20,31,1106,0,36,98,0,0,1002,21,125,20,"+
                   "4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,"+
                   "20,4,20,1105,1,46,98,99",8) == "1000"
assert solve_part2("3,21,1008,21,8,20,1005,20,22,107,8,21,20,"+
                   "1006,20,31,1106,0,36,98,0,0,1002,21,125,20,"+
                   "4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,"+
                   "20,4,20,1105,1,46,98,99",9) == "1001"
assert solve_part2(data, 5) == "7731427"
