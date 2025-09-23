"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 22", "Part 1")
def solve_part1(lines: list[str]):
    """part 1 solving function"""
    return shuffle_idx(lines, 10007, 2019)

@runner("Day 22", "Part 2")
def solve_part2(lines: list[str]):
    """part 2 solving function"""
    return 0

NEW_STACK_INSTRUCT = "deal into new stack"
DEAL_INSTRUCT = "deal with increment "
CUT_INSTRUCT = "cut "

def shuffle_idx(instructions: list[str], size: int, idx: int) -> int:
    """shuffle a deck of supplied size using instructions and follow index"""
    for instruct in instructions:
        if instruct == NEW_STACK_INSTRUCT:
            idx = new_stack_idx(idx, size)
        elif instruct.startswith(DEAL_INSTRUCT):
            increment = int(instruct[len(DEAL_INSTRUCT):])
            idx = deal_stack_idx(idx, increment, size)
        elif instruct.startswith(CUT_INSTRUCT):
            point = int(instruct[len(CUT_INSTRUCT):])
            idx = cut_stack_idx(idx, point, size)
    return idx

def rshuffle_idx(instructions: list[str], size: int, idx: int) -> int:
    """reverse shuffle a deck of supplied size using instructions and follow index"""
    for instruct in reversed(instructions):
        if instruct == NEW_STACK_INSTRUCT:
            idx = new_stack_idx(idx, size)
        elif instruct.startswith(DEAL_INSTRUCT):
            increment = int(instruct[len(DEAL_INSTRUCT):])
            idx = rdeal_stack_idx(idx, increment, size)
        elif instruct.startswith(CUT_INSTRUCT):
            point = int(instruct[len(CUT_INSTRUCT):])
            idx = cut_stack_idx(idx, point * -1, size)
    return idx

def new_stack_idx(idx: int, size: int) -> int:
    """index adjust based on new stack instruction (reverses stack)"""
    return size - idx - 1

assert new_stack_idx(0, 10) == 9
assert new_stack_idx(1, 10) == 8
assert new_stack_idx(2, 10) == 7
assert new_stack_idx(3, 10) == 6
assert new_stack_idx(4, 10) == 5
assert new_stack_idx(5, 10) == 4
assert new_stack_idx(6, 10) == 3
assert new_stack_idx(7, 10) == 2
assert new_stack_idx(8, 10) == 1
assert new_stack_idx(9, 10) == 0

def cut_stack_idx(idx: int, point: int, size: int) -> int:
    """index adjust based on cut instruction"""
    return (idx - point) % size

assert cut_stack_idx(0, 3, 10) == 7
assert cut_stack_idx(1, 3, 10) == 8
assert cut_stack_idx(2, 3, 10) == 9
assert cut_stack_idx(3, 3, 10) == 0
assert cut_stack_idx(4, 3, 10) == 1
assert cut_stack_idx(5, 3, 10) == 2
assert cut_stack_idx(6, 3, 10) == 3
assert cut_stack_idx(7, 3, 10) == 4
assert cut_stack_idx(8, 3, 10) == 5
assert cut_stack_idx(9, 3, 10) == 6
assert cut_stack_idx(0, -4, 10) == 4
assert cut_stack_idx(1, -4, 10) == 5
assert cut_stack_idx(2, -4, 10) == 6
assert cut_stack_idx(3, -4, 10) == 7
assert cut_stack_idx(4, -4, 10) == 8
assert cut_stack_idx(5, -4, 10) == 9
assert cut_stack_idx(6, -4, 10) == 0
assert cut_stack_idx(7, -4, 10) == 1
assert cut_stack_idx(8, -4, 10) == 2
assert cut_stack_idx(9, -4, 10) == 3

# check reverse (original cut point * -1)
assert cut_stack_idx(7, -3, 10) == 0
assert cut_stack_idx(8, -3, 10) == 1
assert cut_stack_idx(9, -3, 10) == 2
assert cut_stack_idx(0, -3, 10) == 3
assert cut_stack_idx(1, -3, 10) == 4
assert cut_stack_idx(2, -3, 10) == 5
assert cut_stack_idx(3, -3, 10) == 6
assert cut_stack_idx(4, -3, 10) == 7
assert cut_stack_idx(5, -3, 10) == 8
assert cut_stack_idx(6, -3, 10) == 9
assert cut_stack_idx(4, 4, 10) == 0
assert cut_stack_idx(5, 4, 10) == 1
assert cut_stack_idx(6, 4, 10) == 2
assert cut_stack_idx(7, 4, 10) == 3
assert cut_stack_idx(8, 4, 10) == 4
assert cut_stack_idx(9, 4, 10) == 5
assert cut_stack_idx(0, 4, 10) == 6
assert cut_stack_idx(1, 4, 10) == 7
assert cut_stack_idx(2, 4, 10) == 8
assert cut_stack_idx(3, 4, 10) == 9

def deal_stack_idx(idx: int, increment: int, size: int) -> int:
    """index adjust based on deal increment"""
    return (idx * increment) % size

assert deal_stack_idx(0, 3, 10) == 0
assert deal_stack_idx(1, 3, 10) == 3
assert deal_stack_idx(2, 3, 10) == 6
assert deal_stack_idx(3, 3, 10) == 9
assert deal_stack_idx(4, 3, 10) == 2
assert deal_stack_idx(5, 3, 10) == 5
assert deal_stack_idx(6, 3, 10) == 8
assert deal_stack_idx(7, 3, 10) == 1
assert deal_stack_idx(8, 3, 10) == 4
assert deal_stack_idx(9, 3, 10) == 7

def rdeal_stack_idx(idx: int, increment: int, size: int) -> int:
    """reverse index adjust based on deal increment"""
    # needed help here:  to reverse needed to do modular inverse which
    # can be accomplished in python using the pow function.
    return (idx * pow(increment, -1, size)) % size

assert rdeal_stack_idx(0, 3, 10) == 0
assert rdeal_stack_idx(3, 3, 10) == 1
assert rdeal_stack_idx(6, 3, 10) == 2
assert rdeal_stack_idx(9, 3, 10) == 3
assert rdeal_stack_idx(2, 3, 10) == 4
assert rdeal_stack_idx(5, 3, 10) == 5
assert rdeal_stack_idx(8, 3, 10) == 6
assert rdeal_stack_idx(1, 3, 10) == 7
assert rdeal_stack_idx(4, 3, 10) == 8
assert rdeal_stack_idx(7, 3, 10) == 9

# Data
data = read_lines("input/day22/input.txt")
sample = """deal with increment 7
deal into new stack
deal into new stack""".splitlines()
sample2 = """cut 6
deal with increment 7
deal into new stack""".splitlines()
sample3 = """deal with increment 7
deal with increment 9
cut -2""".splitlines()
sample4 = """deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1""".splitlines()

# Part 1
assert shuffle_idx(sample, 10, 0) == 0
assert shuffle_idx(sample, 10, 1) == 7
assert shuffle_idx(sample, 10, 2) == 4
assert shuffle_idx(sample, 10, 3) == 1
assert shuffle_idx(sample, 10, 4) == 8
assert shuffle_idx(sample, 10, 5) == 5
assert shuffle_idx(sample, 10, 6) == 2
assert shuffle_idx(sample, 10, 7) == 9
assert shuffle_idx(sample, 10, 8) == 6
assert shuffle_idx(sample, 10, 9) == 3

assert shuffle_idx(sample2, 10, 0) == 1
assert shuffle_idx(sample2, 10, 1) == 4
assert shuffle_idx(sample2, 10, 2) == 7
assert shuffle_idx(sample2, 10, 3) == 0
assert shuffle_idx(sample2, 10, 4) == 3
assert shuffle_idx(sample2, 10, 5) == 6
assert shuffle_idx(sample2, 10, 6) == 9
assert shuffle_idx(sample2, 10, 7) == 2
assert shuffle_idx(sample2, 10, 8) == 5
assert shuffle_idx(sample2, 10, 9) == 8

assert shuffle_idx(sample3, 10, 0) == 2
assert shuffle_idx(sample3, 10, 1) == 5
assert shuffle_idx(sample3, 10, 2) == 8
assert shuffle_idx(sample3, 10, 3) == 1
assert shuffle_idx(sample3, 10, 4) == 4
assert shuffle_idx(sample3, 10, 5) == 7
assert shuffle_idx(sample3, 10, 6) == 0
assert shuffle_idx(sample3, 10, 7) == 3
assert shuffle_idx(sample3, 10, 8) == 6
assert shuffle_idx(sample3, 10, 9) == 9

assert shuffle_idx(sample4, 10, 0) == 7
assert shuffle_idx(sample4, 10, 1) == 4
assert shuffle_idx(sample4, 10, 2) == 1
assert shuffle_idx(sample4, 10, 3) == 8
assert shuffle_idx(sample4, 10, 4) == 5
assert shuffle_idx(sample4, 10, 5) == 2
assert shuffle_idx(sample4, 10, 6) == 9
assert shuffle_idx(sample4, 10, 7) == 6
assert shuffle_idx(sample4, 10, 8) == 3
assert shuffle_idx(sample4, 10, 9) == 0

assert solve_part1(data) == 8502

# Part 2
assert rshuffle_idx(sample, 10, 0) == 0
assert rshuffle_idx(sample, 10, 7) == 1
assert rshuffle_idx(sample, 10, 4) == 2
assert rshuffle_idx(sample, 10, 1) == 3
assert rshuffle_idx(sample, 10, 8) == 4
assert rshuffle_idx(sample, 10, 5) == 5
assert rshuffle_idx(sample, 10, 2) == 6
assert rshuffle_idx(sample, 10, 9) == 7
assert rshuffle_idx(sample, 10, 6) == 8
assert rshuffle_idx(sample, 10, 3) == 9

assert rshuffle_idx(sample2, 10, 1) == 0
assert rshuffle_idx(sample2, 10, 4) == 1
assert rshuffle_idx(sample2, 10, 7) == 2
assert rshuffle_idx(sample2, 10, 0) == 3
assert rshuffle_idx(sample2, 10, 3) == 4
assert rshuffle_idx(sample2, 10, 6) == 5
assert rshuffle_idx(sample2, 10, 9) == 6
assert rshuffle_idx(sample2, 10, 2) == 7
assert rshuffle_idx(sample2, 10, 5) == 8
assert rshuffle_idx(sample2, 10, 8) == 9

assert rshuffle_idx(sample3, 10, 2) == 0
assert rshuffle_idx(sample3, 10, 5) == 1
assert rshuffle_idx(sample3, 10, 8) == 2
assert rshuffle_idx(sample3, 10, 1) == 3
assert rshuffle_idx(sample3, 10, 4) == 4
assert rshuffle_idx(sample3, 10, 7) == 5
assert rshuffle_idx(sample3, 10, 0) == 6
assert rshuffle_idx(sample3, 10, 3) == 7
assert rshuffle_idx(sample3, 10, 6) == 8
assert rshuffle_idx(sample3, 10, 9) == 9

assert rshuffle_idx(sample4, 10, 7) == 0
assert rshuffle_idx(sample4, 10, 4) == 1
assert rshuffle_idx(sample4, 10, 1) == 2
assert rshuffle_idx(sample4, 10, 8) == 3
assert rshuffle_idx(sample4, 10, 5) == 4
assert rshuffle_idx(sample4, 10, 2) == 5
assert rshuffle_idx(sample4, 10, 9) == 6
assert rshuffle_idx(sample4, 10, 6) == 7
assert rshuffle_idx(sample4, 10, 3) == 8
assert rshuffle_idx(sample4, 10, 0) == 9

assert rshuffle_idx(data, 10007, 8502) == 2019

assert solve_part2(data) == 0
