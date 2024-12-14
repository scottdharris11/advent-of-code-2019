"""utility imports"""
from utilities.data import read_lines, parse_integers
from utilities.runner import runner

@runner("Day 2", "Part 1")
def solve_part1(line: str):
    """part 1 solving function"""
    opcodes = parse_integers(line, ",")
    opcodes[1] = 12
    opcodes[2] = 2
    return run_program(opcodes)

@runner("Day 2", "Part 2")
def solve_part2(line: str):
    """part 2 solving function"""
    pgm = parse_integers(line, ",")
    for noun in range(100):
        for verb in range(100):
            opcodes = list(pgm)
            opcodes[1] = noun
            opcodes[2] = verb
            o = run_program(opcodes)
            if o == 19690720:
                return (100 * noun) + verb
    return 0

def run_program(opcodes: list[int]) -> int:
    """run the intcode program and return value"""
    for i in range(0, len(opcodes), 4):
        if opcodes[i] == 99:
            break
        if opcodes[i] == 1:
            opcodes[opcodes[i+3]] = opcodes[opcodes[i+1]] + opcodes[opcodes[i+2]]
        elif opcodes[i] ==2:
            opcodes[opcodes[i+3]] = opcodes[opcodes[i+1]] * opcodes[opcodes[i+2]]
        else:
            print("something broken")
            return None
    return opcodes[0]

# Data
data = read_lines("input/day02/input.txt")[0]

# Part 1
assert run_program(parse_integers("1,9,10,3,2,3,11,0,99,30,40,50",",")) == 3500
assert run_program(parse_integers("1,0,0,0,99",",")) == 2
assert run_program(parse_integers("2,3,0,3,99",",")) == 2
assert run_program(parse_integers("2,4,4,5,99,0",",")) == 2
assert run_program(parse_integers("1,1,1,4,99,5,6,0,99",",")) == 30
assert solve_part1(data) == 3931283

# Part 2
assert solve_part2(data) == 6979
