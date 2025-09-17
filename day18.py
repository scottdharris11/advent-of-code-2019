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
    return best_key_path(KeyState(cave, '@', keys, {}), keys)

@runner("Day 18", "Part 2")
def solve_part2(lines: list[str]) -> int:
    """part 2 solving function"""
    return 0

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
    def __init__(self, cave: Cave, loc: chr, keys: set[chr], cache: dict):
        self.cave = cave
        self.loc = loc
        self.keys = frozenset(keys)
        self.cache = cache

    def path_known(self) -> tuple[bool, int]:
        """determine if the supplied state has been seen and return steps if so"""
        cache_key = (self.loc, self.keys)
        if cache_key in self.cache:
            return True, self.cache[cache_key]
        return False, 0

    def record_path_results(self, steps: int) -> None:
        """cache best path step results from current state"""
        cache_key = (self.loc, self.keys)
        self.cache[cache_key] = steps

    def state_at_key(self, key: chr) -> Self:
        """return new state to represent location at supplied key"""
        nloc = key
        nkeys = set(self.keys)
        nkeys.remove(key)
        return KeyState(self.cave, nloc, nkeys, self.cache)

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

def best_key_path(state: KeyState, outstanding_keys: set[chr]) -> int:
    """find the best path from the supplied location to retrieve all keys"""
    known, steps = state.path_known()
    if known:
        return steps
    steps = 0
    for cost, key in state.potential_moves(outstanding_keys):
        new_state = state.state_at_key(key)
        ccost = best_key_path(new_state, new_state.keys)
        if steps == 0 or cost + ccost < steps:
            steps = cost + ccost
    state.record_path_results(steps)
    return steps

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
