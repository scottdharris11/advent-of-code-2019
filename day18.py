"""utility imports"""
from typing import Self
from utilities.data import read_lines
from utilities.runner import runner
from utilities.search import Search, Searcher, SearchMove

@runner("Day 18", "Part 1")
def solve_part1(lines: list[str]) -> int:
    """part 1 solving function"""
    cave = Cave(lines)
    keys = set(cave.keys_by_name)
    return best_key_path([KeyState(cave, '@', keys)], keys, {})

@runner("Day 18", "Part 2")
def solve_part2(lines: list[str]) -> int:
    """part 2 solving function"""
    vl = len(lines)
    vm = vl // 2
    hl = len(lines[0])
    hm = hl // 2
    lines[vm-1] = lines[vm-1][:hm-1] + "@#@" + lines[vm-1][hm+2:]
    lines[vm] = lines[vm][:hm-1] + "###" + lines[vm][hm+2:]
    lines[vm+1] = lines[vm+1][:hm-1] + "@#@" + lines[vm+1][hm+2:]
    all_keys = set()
    cave_states = []
    for hs, he, vs, ve in [(0,hm+1,0,vm+1),(hm,hl,0,vm+1),(0,hm+1,vm,vl),(hm,hl,vm,vl)]:
        cl = extract_cave(lines, hs, he, vs, ve)
        cave = Cave(cl)
        cave_keys = set(cave.keys_by_name)
        all_keys.update(cave_keys)
        cave_states.append(KeyState(cave, '@', cave_keys))
    return best_key_path(cave_states, all_keys, {})

def extract_cave(lines: list[str], hs: int, he: int, vs: int, ve: int) -> list[str]:
    """extract cave quadraunt"""
    cave_lines = []
    for line in lines[vs:ve]:
        cave_lines.append(line[hs:he])
    return cave_lines

class Cave:
    """structure representing the cave details of the problem space"""
    def __init__(self, lines: list[str]) -> None:
        self.path_maps = None
        self.walls = set()
        self.keys_by_name = {}
        self.doors = {}
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
                        self.keys_by_name[c] = l
                    else:
                        self.doors[l] = c

    def map_paths(self) -> dict[chr,dict[chr,tuple[int,list[str]]]]:
        """map all optimal paths and door blockers"""
        if self.path_maps is not None:
            return self.path_maps
        keys = ['@']
        keys.extend(self.keys_by_name.keys())
        path_maps = {}
        for offset, a in enumerate(keys):
            for b in keys[offset+1:]:
                a_loc = self.key_location(a)
                b_loc = self.key_location(b)
                solution = self.steps_and_doors(a_loc, b_loc)
                if solution is None:
                    continue
                self.add_path_entry(path_maps, a, b, solution)
                self.add_path_entry(path_maps, b, a, solution)
        self.path_maps = path_maps
        return path_maps

    def key_location(self, key: chr) -> tuple[int,int]:
        """get the key location based on name"""
        if key == '@':
            return self.start
        return self.keys_by_name[key]

    def add_path_entry(self, pm: dict, f: chr, t: chr, entry: tuple[int,list[str]]) -> None:
        """add path entry for from/to"""
        from_paths = pm.get(f, {})
        from_paths[t] = entry
        pm[f] = from_paths

    def steps_and_doors(self, s: tuple[int,int], e: tuple[int,int]) -> tuple[int,list[str]]:
        """determine the optimal path between two locations and the doors between"""
        ps = PathSearcher(self.walls, e)
        search = Search(ps)
        solution = search.best(SearchMove(0,s))
        if solution is None:
            return None
        doors = []
        for p in solution.path:
            if p in self.doors:
                doors.append(self.doors[p])
        return (solution.cost, doors)

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
        return abs(self.goal[0]-obj[0]) + abs(self.goal[1]-obj[1])

class KeyState:
    """structure to represent the state of key collection in a cave"""
    def __init__(self, cave: Cave, loc: chr, keys: set[chr]):
        self.cave = cave
        self.loc = loc
        self.keys = frozenset(keys)

    def state_at_key(self, key: chr) -> Self:
        """return new state to represent location at supplied key"""
        nloc = key
        nkeys = set(self.keys)
        nkeys.remove(key)
        return KeyState(self.cave, nloc, nkeys)

    def potential_moves(self, outstanding_keys: set[chr]) -> tuple[int,chr]:
        """based on the current state, determine next potential moves"""
        paths = self.cave.map_paths()[self.loc]
        moves = []
        for loc, (steps, doors) in paths.items():
            if loc not in outstanding_keys:
                continue
            blocked = False
            for door in doors:
                if door.lower() in outstanding_keys:
                    blocked = True
                    break
            if not blocked:
                moves.append((steps, loc))
        return moves

def best_key_path(states: list[KeyState], outstanding_keys: set[chr], cache: dict) -> int:
    """find the best path from the supplied location to retrieve all keys"""
    ck = cache_key(states, outstanding_keys)
    if ck in cache:
        return cache[ck]
    moves = []
    for i, state in enumerate(states):
        for cost, key in state.potential_moves(outstanding_keys):
            moves.append((i,cost,key))
    steps = 0
    for i, cost, key in moves:
        new_states = states[:]
        new_states[i] = states[i].state_at_key(key)
        new_keys = set(outstanding_keys)
        new_keys.remove(key)
        ccost = best_key_path(new_states, new_keys, cache)
        if steps == 0 or cost + ccost < steps:
            steps = cost + ccost
    cache[ck] = steps
    return steps

def cache_key(states: list[KeyState], outstanding_keys: set[chr]) -> tuple:
    """build cache key for list of states and needed keys"""
    ck = []
    for state in states:
        ck.append(state.loc)
    ck.append(frozenset(outstanding_keys))
    return tuple(ck)

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
sample6 = """#######
#a.#Cd#
##...##
##.@.##
##...##
#cB#Ab#
#######""".splitlines()
sample7 = """###############
#d.ABC.#.....a#
######   ######
###### @ ######
######   ######
#b.....#.....c#
###############""".splitlines()
sample8 = """#############
#DcBa.#.GhKl#
#.###   #I###
#e#d# @ #j#k#
###C#   ###J#
#fEbA.#.FgHi#
#############""".splitlines()
sample9 = """#############
#g#f.D#..h#l#
#F###e#E###.#
#dCba   BcIJ#
##### @ #####
#nK.L   G...#
#M###N#H###.#
#o#m..#i#jk.#
#############""".splitlines()


# Part 1
assert solve_part1(sample) == 8
assert solve_part1(sample2) == 86
assert solve_part1(sample3) == 132
assert solve_part1(sample4) == 136
assert solve_part1(sample5) == 81
assert solve_part1(data) == 7048

# Part 2
assert solve_part2(sample6) == 8
assert solve_part2(sample7) == 24
assert solve_part2(sample8) == 32
assert solve_part2(sample9) == 72
assert solve_part2(data) == 1836
