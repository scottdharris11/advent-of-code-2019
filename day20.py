"""utility imports"""
from typing import TypeAlias
from utilities.data import read_lines
from utilities.runner import runner
from utilities.search import Search, Searcher, SearchMove

@runner("Day 20", "Part 1")
def solve_part1(lines: list[str]):
    """part 1 solving function"""
    maze = Maze(lines)
    aa = maze.label_points['AA'][0]
    zz = maze.label_points['ZZ'][0]
    return best_route(aa, zz, 0, [aa], maze)

@runner("Day 20", "Part 2")
def solve_part2(lines: list[str]):
    """part 2 solving function"""
    return 0

Point: TypeAlias = tuple[int,int]

class Maze:
    """structure representing maze"""
    def __init__(self, lines: list[str]):
        self.spaces = set()
        self.labels = set()
        self.portals = {}
        self.label_points = {}
        self.point_labels = {}
        self.route_cache = None
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c in (' ', '#'):
                    continue
                point = (x,y)
                if c == '.':
                    self.spaces.add(point)
                else:
                    if point in self.labels:
                        continue
                    lbl, lpoint, spoint = self.extract_label(point, lines)
                    self.labels.add(point)
                    self.labels.add(lpoint)
                    lp = self.label_points.get(lbl, [])
                    lp.append(spoint)
                    self.label_points[lbl] = lp
                    self.point_labels[spoint] = lbl
        for lp in self.label_points.values():
            if len(lp) != 2:
                continue
            self.portals[lp[0]] = lp[1]
            self.portals[lp[1]] = lp[0]

    def extract_label(self, point: Point, lines: list[str]) -> tuple:
        """extract the label that starts at the supplied point"""
        label = lines[point[1]][point[0]]
        for la, sa in [((0,1),(0,2)),((0,1),(0,-1)),((1,0),(2,0)),((1,0),(-1,0))]:
            lx = point[0] + la[0]
            ly = point[1] + la[1]
            sx = point[0] + sa[0]
            sy = point[1] + sa[1]
            if len(lines) > sy and len(lines[sy]) > sx and \
                lines[ly][lx] not in (' ', '.', '#') and lines[sy][sx] == '.':
                label += lines[ly][lx]
                break
        return (label, (lx,ly), (sx,sy))

    def routes(self) -> dict[str,list[tuple[str,int]]]:
        """compute all the possible routes between different portal labels"""
        if self.route_cache is not None:
            return self.route_cache
        points = list(self.point_labels.keys())
        r = {}
        for i, a in enumerate(points):
            a_lbl = self.point_labels[a]
            for b in points[i:]:
                b_lbl = self.point_labels[b]
                if a_lbl == b_lbl:
                    continue
                ps = PathSearcher(self, b)
                search = Search(ps)
                solution = search.best(SearchMove(0,a))
                if solution is None:
                    continue
                add_route(r, a, b, solution.cost)
                add_route(r, b, a, solution.cost)
        self.route_cache = r
        return r

def add_route(routes: dict, f: Point, t: Point, steps: int) -> None:
    """add route between labels"""
    l = routes.get(f, [])
    l.append((t, steps))
    routes[f] = l

class PathSearcher(Searcher):
    """path search implementation for the area"""
    def __init__(self, maze: Maze, goal: Point) -> None:
        self.maze = maze
        self.goal = goal

    def is_goal(self, obj: Point) -> bool:
        """determine if the supplied state is the goal location"""
        return obj == self.goal

    def possible_moves(self, obj: Point) -> list[SearchMove]:
        """determine possible moves from curent location"""
        moves = []
        for m in [(1,0),(-1,0),(0,1),(0,-1)]:
            loc = (obj[0] + m[0], obj[1] + m[1])
            if loc not in self.maze.spaces:
                continue
            moves.append(SearchMove(1,loc))
        return moves

    def distance_from_goal(self, obj: Point) -> int:
        """calculate distance from the goal"""
        return abs(self.goal[0]-obj[0]) + abs(self.goal[1]-obj[1])

def best_route(point: Point, goal: Point, steps: int, visited: list[Point], maze: Maze) -> int:
    """find the best route between to the goal"""
    if point == goal:
        #print(f"route found ({steps}): {visited}")
        return steps
    if point in maze.portals:
        steps += 1 # cost of using a portal
        point = maze.portals[point]
    cost = 0
    for p, s in maze.routes()[point]:
        if p in visited:
            continue
        nvisited = list(visited)
        nvisited.append(p)
        cc = best_route(p, goal, steps+s, nvisited, maze)
        if cc > 0 and (cost == 0 or cc < cost):
            cost = cc
    return cost

# Data
data = read_lines("input/day20/input.txt")
sample = """         A           
         A           
  #######.#########  
  #######.........#  
  #######.#######.#  
  #######.#######.#  
  #######.#######.#  
  #####  B    ###.#  
BC...##  C    ###.#  
  ##.##       ###.#  
  ##...DE  F  ###.#  
  #####    G  ###.#  
  #########.#####.#  
DE..#######...###.#  
  #.#########.###.#  
FG..#########.....#  
  ###########.#####  
             Z       
             Z       """.splitlines()
sample2 = """                   A               
                   A               
  #################.#############  
  #.#...#...................#.#.#  
  #.#.#.###.###.###.#########.#.#  
  #.#.#.......#...#.....#.#.#...#  
  #.#########.###.#####.#.#.###.#  
  #.............#.#.....#.......#  
  ###.###########.###.#####.#.#.#  
  #.....#        A   C    #.#.#.#  
  #######        S   P    #####.#  
  #.#...#                 #......VT
  #.#.#.#                 #.#####  
  #...#.#               YN....#.#  
  #.###.#                 #####.#  
DI....#.#                 #.....#  
  #####.#                 #.###.#  
ZZ......#               QG....#..AS
  ###.###                 #######  
JO..#.#.#                 #.....#  
  #.#.#.#                 ###.#.#  
  #...#..DI             BU....#..LF
  #####.#                 #.#####  
YN......#               VT..#....QG
  #.###.#                 #.###.#  
  #.#...#                 #.....#  
  ###.###    J L     J    #.#.###  
  #.....#    O F     P    #.#...#  
  #.###.#####.#.#####.#####.###.#  
  #...#.#.#...#.....#.....#.#...#  
  #.#####.###.###.#.#.#########.#  
  #...#.#.....#...#.#.#.#.....#.#  
  #.###.#####.###.###.#.#.#######  
  #.#.........#...#.............#  
  #########.###.###.#############  
           B   J   C               
           U   P   P               """.splitlines()

# Part 1
assert solve_part1(sample) == 23
assert solve_part1(sample2) == 58
assert solve_part1(data) == 658

# Part 2
assert solve_part2(sample) == 0
assert solve_part2(sample2) == 0
assert solve_part2(data) == 0
