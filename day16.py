"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 16", "Part 1")
def solve_part1(line: str, phase_cnt: int) -> str:
    """part 1 solving function"""
    isignal = [int(ch) for ch in line]
    return signal_after_phase(isignal, phase_cnt)

@runner("Day 16", "Part 2")
def solve_part2(line: str, phase_cnt: int) -> int:
    """part 2 solving function"""
    isignal = [int(ch) for ch in line] * 10000
    return signal_after_phase(isignal, phase_cnt)

class RepeatPattern:
    """structure to enable applying repeating pattern"""
    def __init__(self, position: int):
        self.seq = [0, 1, 0, -1]
        self.seq_len = len(self.seq)
        self.position = position
        self.seq_idx = 0
        self.seq_apply = position - 1
        if self.seq_apply == 0:
            self.seq_idx = 1
            self.seq_apply = position

    def next_pattern(self) -> tuple[int,int]:
        """provide back next multiplier and steps"""
        pattern = (self.seq[self.seq_idx],self.seq_apply)
        self.seq_idx += 1
        self.seq_apply = self.position
        if self.seq_idx == self.seq_len:
            self.seq_idx = 0
        return pattern

def signal_after_phase(isignal: list[int], phase_cnt: int) -> str:
    """compute the first 8 bytes of the output signal after applying number of phases"""
    osignal = [0] * len(isignal)
    for p in range(phase_cnt):
        print(f"Phase {p+1} of {phase_cnt}")
        phase(isignal, osignal)
        isignal, osignal = osignal, isignal
    return "".join([str(i) for i in isignal[0:8]])

def phase(isignal: list[int], osignal: list[int]) -> None:
    """transform a signal within a phase"""
    slen = len(isignal)
    for idx in range(slen):
        osignal[idx] = phase_signal_position(isignal, idx+1, slen)
        if idx % 1000 == 0:
            print(f"Signal Index {idx+1} of {slen}, Output: {osignal[idx]}")

def phase_signal_position(signal: list[int], position: int, signal_len: int) -> int:
    """calculate the next phase value for the supplied position"""
    rp = RepeatPattern(position)
    mul, steps = rp.next_pattern()
    idx = 0
    value = 0
    while idx < signal_len:
        if mul == 1:
            value += sum(signal[idx:idx+steps])
        elif mul == -1:
            value -= sum(signal[idx:idx+steps])
        idx += steps
        mul, steps = rp.next_pattern()
        if idx + steps >= signal_len:
            steps = signal_len - idx
    value = abs(value) % 10
    return value

# Data
data = read_lines("input/day16/input.txt")[0]
sample = """12345678""".splitlines()[0]
sample2 = """80871224585914546619083218645595""".splitlines()[0]
sample3 = """19617804207202209144916044189917""".splitlines()[0]
sample4 = """69317163492948606335995924319873""".splitlines()[0]
sample5 = """03036732577212944063491565474664""".splitlines()[0]
sample6 = """02935109699940807407585447034323""".splitlines()[0]
sample7 = """03081770884921959731165446850517""".splitlines()[0]

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
assert solve_part2(sample5, 100) == "84462026"
assert solve_part2(sample6, 100) == "78725270"
assert solve_part2(sample7, 100) == "53553731"
#assert solve_part2(data, 100) == ""
