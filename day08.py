"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 8", "Part 1")
def solve_part1(line: str, wide: int, tall: int):
    """part 1 solving function"""
    chunk_size = wide * tall
    zero_min = None
    ones_times_twos = 0
    for i in range(0,len(line),chunk_size):
        dcounts = {}
        for d in line[i:i+chunk_size]:
            dcounts[d] = dcounts.get(d,0) + 1
        zeros = dcounts.get('0',0)
        if zero_min is None or zeros < zero_min:
            zero_min = zeros
            ones_times_twos = dcounts.get('1',0) * dcounts.get('2',0)
    return ones_times_twos

@runner("Day 8", "Part 2")
def solve_part2(line: str, wide: int, tall: int):
    """part 2 solving function"""
    pixels = []
    for _ in range(tall):
        pixels.append(['2']*wide)
    chunk_size = wide * tall
    for i in range(0,len(line),chunk_size):
        chunk = line[i:i+chunk_size]
        ri = 0
        for r in range(0,len(chunk),wide):
            row = line[i+r:i+r+wide]
            for ci, col in enumerate(row):
                if pixels[ri][ci] != '2':
                    continue
                if col in ['0', '1']:
                    pixels[ri][ci] = col
            ri += 1
    rows = ["".join(x).replace('0',' ') for x in pixels]
    return "\n".join(rows)

# Data
data = read_lines("input/day08/input.txt")[0]
sample = """123456789012""".splitlines()[0]
sample2 = """0222112222120000""".splitlines()[0]

# Part 1
assert solve_part1(sample, 3, 2) == 1
assert solve_part1(data, 25, 6) == 1792

# Part 2
assert solve_part2(sample2, 2, 2) == """ 1
1 """
assert solve_part2(data, 25, 6) == """1      11 1111  11  1  1 
1       1 1    1  1 1  1 
1       1 111  1    1111 
1       1 1    1    1  1 
1    1  1 1    1  1 1  1 
1111  11  1111  11  1  1 """ #LJECH
