"""utility imports"""
import math
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 14", "Part 1")
def solve_part1(lines: list[str]):
    """part 1 solving function"""
    recipes = parse_input(lines)
    fuel = recipes["FUEL"]
    fuel = expand_to_ore_based(fuel, recipes)
    ore = 0
    for c, q in fuel.ingredients.items():
        cr = recipes[c]
        ore += math.ceil(q / cr.quantity) * cr.ingredients["ORE"]
    return ore

@runner("Day 14", "Part 2")
def solve_part2(lines: list[str]):
    """part 2 solving function"""
    return 0

class Recipe:
    """structure for chemical reaction"""
    def __init__(self, line: str):
        i, o = tuple(line.split(" => "))
        q, c = tuple(o.split(" "))
        self.quantity = int(q)
        self.chemical = c
        self.ingredients = {}
        self.ore_based = False
        for x in i.split(", "):
            q, c = tuple(x.split(" "))
            self.ingredients[c] = int(q)
            if c == "ORE":
                self.ore_based = True

    def __repr__(self):
        return str((self.chemical, self.quantity, self.ore_based, self.ingredients))

def expand_to_ore_based(fuel: Recipe, recipes: dict[str,Recipe]) -> Recipe:
    """expand the fuel ingredients so they are only ore-based"""
    initial = True
    while True:
        # Focus on expanding chemicals not made up of fully ore-based
        # ingredients initially to determine the least amount of values
        # needed from ore-based ingredients.
        if not expand_ingredients(fuel, recipes, initial):
            if initial:
                initial = False
            else:
                break
    return fuel

def expand_ingredients(fuel: Recipe, recipes: dict[str,Recipe], initial: bool) -> bool:
    """expand the non-orebased ingredients and return if there are more"""
    expanded = {}
    more_needed = False
    for chemical, qty in fuel.ingredients.items():
        cr = recipes[chemical]
        ingredients_all_ore_based = False
        # only focus on expanding chemicals not made up of fully ore-based
        # ingredients initially to determine the least amount of values
        # needed from ore-based ingredients.
        if initial is True and not cr.ore_based:
            ingredients_all_ore_based = True
            for c, _ in cr.ingredients.items():
                if not recipes[c].ore_based:
                    ingredients_all_ore_based = False
                    break
        if cr.ore_based or ingredients_all_ore_based:
            expanded[chemical] = qty + expanded.get(chemical,0)
            continue
        for c, q in cr.ingredients.items():
            expanded[c] = (q*math.ceil(qty/cr.quantity)) + expanded.get(c,0)
            if not recipes[c].ore_based:
                more_needed = True
    fuel.ingredients = expanded
    return more_needed

def parse_input(lines: list[str]) -> dict[str,Recipe]:
    """parse input lines into recipies"""
    recipes = {}
    for line in lines:
        r = Recipe(line)
        recipes[r.chemical] = r
    return recipes

# Data
data = read_lines("input/day14/input.txt")
sample = """10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL""".splitlines()
sample2 = """9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL""".splitlines()
sample3 = """157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT""".splitlines()
sample4 = """2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF""".splitlines()
sample5 = """171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX""".splitlines()

# Part 1
assert solve_part1(sample) == 31
assert solve_part1(sample2) == 165
assert solve_part1(sample3) == 13312
assert solve_part1(sample4) == 180697
assert solve_part1(sample5) == 2210736
assert solve_part1(data) < 1045824 ##too high

# Part 2
assert solve_part2(sample) == 0
assert solve_part2(data) == 0
