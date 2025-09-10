"""utility imports"""
from utilities.data import read_lines, parse_integers
from utilities.runner import runner
from utilities.search import Search, Searcher, SearchMove

@runner("Day 15", "Part 1")
def solve_part1(line: str) -> int:
    """part 1 solving function"""
    oc = parse_integers(line, ",")
    io = IOProvider()
    computer = Computer(oc, io)
    computer.run()
    s = Search(PathSearcher(set(io.spaces.keys()), io.goal))
    solution = s.best(SearchMove(0, (0,0)))
    return len(solution.path) - 1

@runner("Day 15", "Part 2")
def solve_part2(line: str) -> int:
    """part 2 solving function"""
    oc = parse_integers(line, ",")
    io = IOProvider()
    computer = Computer(oc, io)
    computer.run()
    spaces = io.spaces
    for k in spaces:
        spaces[k] = -1
    fill_oxygen(io.goal, spaces, 0)
    fill_time = 0
    for minute in spaces.values():
        fill_time = max(fill_time, minute)
    return fill_time

NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4
MOVES = {NORTH: (0,-1), SOUTH: (0,1), WEST: (-1,0), EAST: (1,0)}

def fill_oxygen(loc: tuple[int,int], spaces: dict[tuple[int,int],int], minute: int):
    """recursively fill oxygen for all spaces in the minimum time"""
    spaces[loc] = minute
    fill_minute = minute + 1
    for move in MOVES.values():
        nloc = (loc[0]+move[0],loc[1]+move[1])
        if nloc not in spaces:
            continue
        fill = spaces[nloc]
        if fill == -1 or fill_minute < fill:
            fill_oxygen(nloc, spaces, fill_minute)

def md(a: tuple[int,int], b: tuple[int,int]) -> int:
    """compute the manhattan distance between two points"""
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

class PathSearcher(Searcher):
    """path search implementation for the area"""
    def __init__(self, spaces: set[tuple[int,int]], g: tuple[int,int]) -> None:
        self.spaces = spaces
        self.goal = g

    def is_goal(self, obj: tuple[int,int]) -> bool:
        """determine if the supplied state is the goal location"""
        return obj == self.goal

    def possible_moves(self, obj: tuple[int,int]) -> list[SearchMove]:
        """determine possible moves from curent location"""
        moves = []
        for m in [(1,0),(-1,0),(0,1),(0,-1)]:
            loc = (obj[0] + m[0], obj[1] + m[1])
            if loc not in self.spaces:
                continue
            moves.append(SearchMove(1,loc))
        return moves

    def distance_from_goal(self, obj: tuple[int,int]) -> int:
        """calculate distance from the goal"""
        return md(self.goal, obj)

class IOProvider:
    """structure for fixing robot"""
    def __init__(self):
        self.current = (0,0)
        self.goal = None
        self.spaces = {}
        self.spaces[self.current] = 1
        self.walls = set()
        self.last_direction = None
        self.space_count = 1
        self.outputs_since_change = 0

    def provide_input(self):
        """provide input to the robot based on current location. will
        pick direction that has been visited the least amount of times"""
        move = 0
        vc = 999999
        for direction, adjust in MOVES.items():
            position = (self.current[0]+adjust[0], self.current[1]+adjust[1])
            if position in self.walls:
                continue
            count = self.spaces.get(position,0)
            if count < vc:
                move = direction
                vc = count
        self.last_direction = move
        return move

    def accept_output(self, o: int):
        """accept output value and record mapping actions accordingly"""
        move = MOVES[self.last_direction]
        position = (self.current[0]+move[0], self.current[1]+move[1])
        if o == 0: # hit wall
            self.walls.add(position)
            return
        self.spaces[position] = self.spaces.get(position,0) + 1
        self.current = position
        if o == 2: # found goal space
            self.goal = position

    def halt_program(self) -> bool:
        """exit point to stop program once goal is reached and no 
        more new spaces have been discovered recently"""
        if self.goal is None:
            return False
        sc = len(self.spaces)
        if sc == self.space_count:
            self.outputs_since_change += 1
        else:
            self.space_count = sc
            self.outputs_since_change = 0
        return self.outputs_since_change > 20000

class Computer:
    """structure for computer"""
    def __init__(self, op: list[int], io: IOProvider):
        self.op = {i:o for i, o in enumerate(op)}
        self.io = io
        self.opi = 0
        self.relative_base = 0
        self.done = False

    def run(self) -> bool:
        """run the intcode program and return value"""
        i = self.opi
        while i < len(self.op):
            opcode, m1, m2, m3 = self.opcode_modes(self.opc(i))
            if opcode == 99 or self.io.halt_program():
                self.done = True
                break
            if opcode == 1:
                self.op[self.pvi(i+3,m3)] = self.pv(i+1,m1) + self.pv(i+2,m2)
                i += 4
            elif opcode == 2:
                self.op[self.pvi(i+3,m3)] = self.pv(i+1,m1) * self.pv(i+2,m2)
                i += 4
            elif opcode == 3:
                self.op[self.pvi(i+1,m1)] = self.io.provide_input()
                i += 2
            elif opcode == 4:
                self.io.accept_output(self.pv(i+1,m1))
                i += 2
            elif opcode == 5:
                if self.pv(i+1,m1) != 0:
                    i = self.pv(i+2,m2)
                else:
                    i += 3
            elif opcode == 6:
                if self.pv(i+1,m1) == 0:
                    i = self.pv(i+2,m2)
                else:
                    i += 3
            elif opcode == 7:
                self.op[self.pvi(i+3,m3)] = 1 if self.pv(i+1,m1) < self.pv(i+2,m2) else 0
                i += 4
            elif opcode == 8:
                self.op[self.pvi(i+3,m3)] = 1 if self.pv(i+1,m1) == self.pv(i+2,m2) else 0
                i += 4
            elif opcode == 9:
                self.relative_base += self.pv(i+1,m1)
                i += 2
        self.opi = i

    def opc(self, i: int) -> int:
        """get the value of supplied index"""
        return self.op.get(i, 0)

    def opcode_modes(self, o: int) -> tuple[int,int,int,int]:
        """parse opcode and modes from input"""
        mode3 = 0
        if o > 20000:
            mode3 = 2
            o -= 20000
        elif o > 10000:
            mode3 = 1
            o -= 10000
        mode2 = 0
        if o > 2000:
            mode2 = 2
            o -= 2000
        elif o > 1000:
            mode2 = 1
            o -= 1000
        mode1 = 0
        if o > 200:
            mode1 = 2
            o -= 200
        elif o > 100:
            mode1 = 1
            o -= 100
        return o, mode1, mode2, mode3

    def pv(self, idx: int, mode: int) -> int:
        """determine proper param value based on index and mode"""
        if mode == 0:
            return self.opc(self.opc(idx))
        if mode == 1:
            return self.opc(idx)
        return self.opc(self.opc(idx) + self.relative_base)

    def pvi(self, idx: int, mode: int) -> int:
        """determine proper param value index based on index and mode"""
        if mode in [0,1]:
            return self.opc(idx)
        return self.opc(idx) + self.relative_base

# Data
data = read_lines("input/day15/input.txt")[0]

# Part 1
assert solve_part1(data) == 212

# Part 2
assert solve_part2(data) == 358
