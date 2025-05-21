"""utility imports"""
from utilities.data import read_lines, parse_integers
from utilities.runner import runner

@runner("Day 7", "Part 1")
def solve_part1(line: str):
    """part 1 solving function"""
    opcodes = parse_integers(line, ",")
    sequences = set()
    phase_sequences(0, 4, 5, tuple(), sequences)
    return max_output_signal(opcodes, sequences, False)

@runner("Day 7", "Part 2")
def solve_part2(line: str):
    """part 2 solving function"""
    opcodes = parse_integers(line, ",")
    sequences = set()
    phase_sequences(5, 9, 5, tuple(), sequences)
    return max_output_signal(opcodes, sequences, True)

def phase_sequences(min_phase: int, max_phase: int, to_assign: int, values: tuple, sequences: set):
    """build unique sequences"""
    if to_assign == 0:
        sequences.add(values)
        return
    for p in range(min_phase, max_phase+1):
        if p in values:
            continue
        v = list(values)
        v.append(p)
        phase_sequences(min_phase, max_phase, to_assign-1, tuple(v), sequences)

def max_output_signal(opcodes: list[int], sequences: set, loop: bool) -> int:
    """find the maximum output signal"""
    max_output = 0
    for seq in sequences:
        os = output_signal(opcodes, seq, loop)
        if os > max_output:
            max_output = os
    return max_output

def output_signal(opcodes: list[int], phases: set, loop: bool) -> int:
    """compute the output signal for the phase sequence"""
    amps = []
    for phase in phases:
        amp = Amplifier(list(opcodes))
        amp.in_signals.append(phase)
        amps.append(amp)
    for i in range(1,len(amps)):
        amps[i-1].out_signals = amps[i].in_signals
    if loop:
        amps[-1].out_signals = amps[0].in_signals
    amps[0].in_signals.append(0)
    while True:
        alldone = True
        for amp in amps:
            if amp.done:
                continue
            alldone = False
            amp.run()
        if alldone:
            break
    return amps[-1].out_signals[-1]

class Amplifier:
    """structure for amplifier"""
    def __init__(self, op: list[int]):
        self.op = op
        self.in_signals = []
        self.out_signals = []
        self.opi = 0
        self.done = False

    def run(self):
        """run the intcode program and return value"""
        i = self.opi
        while i < len(self.op):
            opcode, m1, m2, _ = opcode_modes(self.op[i])
            if opcode == 99:
                self.done = True
                break
            if opcode == 1:
                self.op[pv(self.op,i+3,1)] = pv(self.op,i+1,m1) + pv(self.op,i+2,m2)
                i += 4
            elif opcode == 2:
                self.op[pv(self.op,i+3,1)] = pv(self.op,i+1,m1) * pv(self.op,i+2,m2)
                i += 4
            elif opcode == 3:
                if len(self.in_signals) == 0:
                    break
                self.op[pv(self.op,i+1,1)] = self.in_signals.pop(0)
                i += 2
            elif opcode == 4:
                self.out_signals.append(pv(self.op,i+1,m1))
                i += 2
            elif opcode == 5:
                if pv(self.op,i+1,m1) != 0:
                    i = pv(self.op,i+2,m2)
                else:
                    i += 3
            elif opcode == 6:
                if pv(self.op,i+1,m1) == 0:
                    i = pv(self.op,i+2,m2)
                else:
                    i += 3
            elif opcode == 7:
                self.op[pv(self.op,i+3,1)] = 1 if pv(self.op,i+1,m1) < pv(self.op,i+2,m2) else 0
                i += 4
            elif opcode == 8:
                self.op[pv(self.op,i+3,1)] = 1 if pv(self.op,i+1,m1) == pv(self.op,i+2,m2) else 0
                i += 4
        self.opi = i

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
SAMPLE = "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"
SAMPLE2 = "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0"
SAMPLE3 = "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31," + \
    "31,1,32,31,31,4,31,99,0,0,03,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"
SAMPLE4 = "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005," + \
    "28,6,99,0,0,5"
SAMPLE5 = "3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54," + \
    "1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56," + \
    "1005,56,6,99,0,0,0,0,10"

# Part 1
assert solve_part1(SAMPLE) == 43210
assert solve_part1(SAMPLE2) == 54321
assert solve_part1(SAMPLE3) == 65210
assert solve_part1(data) == 255590

# Part 2
assert solve_part2(SAMPLE4) == 139629729
assert solve_part2(SAMPLE5) == 18216
assert solve_part2(data) == 58285150
