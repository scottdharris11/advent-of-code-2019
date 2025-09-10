"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 16", "Part 1")
def solve_part1(line: str, phase_cnt: int) -> str:
    """part 1 solving function"""
    signal = [int(ch) for ch in line]
    for _ in range(phase_cnt):
        signal = phase(signal)
    return "".join([str(i) for i in signal[0:8]])

@runner("Day 16", "Part 2")
def solve_part2(lines: list[str]) -> int:
    """part 2 solving function"""
    return 0

class RepeatPattern:
    """structure to enable applying repeating pattern"""
    def __init__(self, position: int):
        self.seq = [0, 1, 0, -1]
        self.position = position
        self.seq_idx = 0
        self.seq_idx_apply = 1

    def multiplier(self) -> int:
        """determine the next multiplier to use"""
        if self.seq_idx_apply == self.position:
            self.seq_idx += 1
            if self.seq_idx == len(self.seq):
                self.seq_idx = 0
            self.seq_idx_apply = 0
        self.seq_idx_apply += 1
        return self.seq[self.seq_idx]

def phase(signal: list[int]) -> list[int]:
    """transform a signal within a phase"""
    osignal = []
    slen = len(signal)
    for idx in range(slen):
        osignal.append(phase_signal_position(signal, idx+1))
    return osignal

def phase_signal_position(signal: list[int], position: int) -> int:
    """calculate the next phase value for the supplied position"""
    pattern = RepeatPattern(position)
    value = 0
    for s in signal:
        value += s * pattern.multiplier()
    value = abs(value) % 10
    return value

# Data
data = read_lines("input/day16/input.txt")[0]
sample = """12345678""".splitlines()[0]
sample2 = """80871224585914546619083218645595""".splitlines()[0]
sample3 = """19617804207202209144916044189917""".splitlines()[0]
sample4 = """69317163492948606335995924319873""".splitlines()[0]

# Part 1
assert solve_part1(sample, 1) == "48226158"
assert solve_part1(sample, 2) == "34040438"
assert solve_part1(sample, 3) == "03415518"
assert solve_part1(sample, 4) == "01029498"
assert solve_part1(sample2, 100) == "24176176"
assert solve_part1(sample3, 100) == "73745418"
assert solve_part1(sample4, 100) == "52432133"
assert solve_part1(data, 100) == "11833188"

# Part 2
assert solve_part2(sample) == 0
assert solve_part2(data) == 0
