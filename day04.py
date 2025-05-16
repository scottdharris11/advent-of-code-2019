"""utility imports"""
from utilities.runner import runner

@runner("Day 4", "Part 1")
def solve_part1(line: str):
    """part 1 solving function"""
    rmin, rmax, *_ = (int(x) for x in line.split("-"))
    count = 0
    for pwd in range(rmin, rmax+1):
        if valid(str(pwd)):
            count += 1
    return count

@runner("Day 4", "Part 2")
def solve_part2(line: str):
    """part 2 solving function"""
    rmin, rmax, *_ = (int(x) for x in line.split("-"))
    count = 0
    for pwd in range(rmin, rmax+1):
        if extended_valid(str(pwd)):
            count += 1
    return count

def valid(pwd: str) -> bool:
    """check if password could be valid"""
    dup = False
    prev = None
    for p in pwd:
        if prev is not None:
            if prev > p:
                return False
            if prev == p:
                dup = True
        prev = p
    return dup

def extended_valid(pwd: str) -> bool:
    """check if password could be valid"""
    dups = {}
    prev = None
    for p in pwd:
        if prev is not None:
            if prev > p:
                return False
            if prev == p:
                dups[p] = dups.get(p, 1) + 1
        prev = p
    return 2 in dups.values()

# Part 1
assert valid("111111") is True
assert valid("223450") is False
assert valid("123789") is False
assert solve_part1("134792-675810") == 1955

# Part 2
assert extended_valid("112233") is True
assert extended_valid("123444") is False
assert extended_valid("111122") is True
assert solve_part2("134792-675810") == 1319
