"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner
from utilities.search import Search, Searcher, SearchMove, SearchSolution

@runner("Day 18", "Part 1")
def solve_part1(lines: list[str]) -> int:
    """part 1 solving function"""
    cave = Cave(lines)
    return cave.min_key_path()

@runner("Day 18", "Part 2")
def solve_part2(lines: list[str]) -> int:
    """part 2 solving function"""
    return 0

class Cave:
    """structure representing the cave details of the problem space"""
    def __init__(self, lines: list[str]) -> None:
        self.path_cache = {}
        self.walls = set()
        self.keys = {}
        self.keys_by_name = {}
        self.doors = {}
        self.doors_by_name = {}
        self.start = None
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                l = (x,y)
                if c == '#':
                    self.walls.add(l)
                elif c == '@':
                    self.start = l
                elif c.isalpha():
                    if c.islower():
                        self.keys[l] = c
                        self.keys_by_name[c] = l
                    else:
                        self.doors[l] = c
                        self.doors_by_name[c] = l

    def min_key_path(self) -> int:
        """determine the path to retrieve all keys that takes the least steps"""
        keys = set(self.keys_by_name.keys())
        return self.best_path(self.start, keys)

    def path_from_to(self, s: tuple[int,int], key: chr, keys: set[chr]) -> SearchSolution:
        """find the path from starting location with the supplied set of keys still active"""
        goal = self.keys_by_name[key]
        walls = set(self.walls)
        for k in keys:
            d = k.upper()
            if d in self.doors_by_name:
                walls.add(self.doors_by_name[d])
        ps = PathSearcher(walls, goal)
        search = Search(ps)
        solution = search.best(SearchMove(0,s))
        if solution is not None:
            for p in solution.path:
                if p == s or p == goal:
                    continue
                if p in self.keys:
                    if self.keys[p] in keys:
                        return None
        return solution

    def best_path(self, loc: tuple[int,int], keys: set[chr]) -> int:
        """find the best path from the supplied location to retrieve all keys"""
        ckey = (loc, frozenset(keys))
        if ckey in self.path_cache:
            return self.path_cache[ckey]
        steps = 0
        for key in keys:
            solution = self.path_from_to(loc, key, keys)
            if solution is None:
                continue
            cost = solution.cost
            nkeys = set(keys)
            nkeys.remove(key)
            ccost = 0
            if len(nkeys) > 0:
                ccost = self.best_path(self.keys_by_name[key], nkeys)
                if ccost == 0:
                    continue
            if steps == 0 or cost + ccost < steps:
                steps = cost + ccost
        self.path_cache[ckey] = steps
        return steps

class PathSearcher(Searcher):
    """path search implementation for the area"""
    def __init__(self, walls: set[tuple[int,int]], goal: tuple[int,int]) -> None:
        self.walls = walls
        self.goal = goal

    def is_goal(self, obj: tuple[int,int]) -> bool:
        """determine if the supplied state is the goal location"""
        return obj == self.goal

    def possible_moves(self, obj: tuple[int,int]) -> list[SearchMove]:
        """determine possible moves from curent location"""
        moves = []
        for m in [(1,0),(-1,0),(0,1),(0,-1)]:
            loc = (obj[0] + m[0], obj[1] + m[1])
            if loc in self.walls:
                continue
            moves.append(SearchMove(1,loc))
        return moves

    def distance_from_goal(self, obj: tuple[int,int]) -> int:
        """calculate distance from the goal"""
        return md(self.goal, obj)

def md(a: tuple[int,int], b: tuple[int,int]) -> int:
    """compute the manhattan distance between two points"""
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

# Data
data = read_lines("input/day18/input.txt")
sample = """#########
#b.A.@.a#
#########""".splitlines()
sample2 = """########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################""".splitlines()
sample3 = """########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################""".splitlines()
sample4 = """#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################""".splitlines()
sample5 = """########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################""".splitlines()

# Part 1
assert solve_part1(sample) == 8
assert solve_part1(sample2) == 86
assert solve_part1(sample3) == 132
assert solve_part1(sample4) == 136
assert solve_part1(sample5) == 81
assert solve_part1(data) == 7048

# Part 2
assert solve_part2(sample) == 0
assert solve_part2(data) == 0
