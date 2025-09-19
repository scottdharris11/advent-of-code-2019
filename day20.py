"""utility imports"""
from typing import TypeAlias
from utilities.data import read_lines
from utilities.runner import runner
from utilities.search import Search, Searcher, SearchMove

@runner("Day 20", "Part 1")
def solve_part1(lines: list[str]):
    """part 1 solving function"""
    maze = Maze(lines, False, 0)
    visited = set()
    visited.add((0,maze.start))
    return best_route((0,maze.start), (0,maze.end), visited, maze)

@runner("Day 20", "Part 2")
def solve_part2(lines: list[str], max_recurse: int):
    """part 2 solving function"""
    maze = Maze(lines, True, max_recurse)
    visited = set()
    visited.add((0,maze.start))
    return best_route((0,maze.start), (0,maze.end), visited, maze)

Point: TypeAlias = tuple[int,int]
LevelPoint: TypeAlias = tuple[int,Point]

class Maze:
    """structure representing maze"""
    def __init__(self, lines: list[str], recursive: bool, max_recurse: int):
        self.spaces = set()
        self.portals = {}
        self.outer_portals = set()
        self.point_labels = {}
        self.routes_cache = None
        self.start = None
        self.end = None
        self.recursive = recursive
        self.max_recurse = max_recurse

        # process grid initially
        labels = set()
        label_points = {}
        min_y, max_y, min_x, max_x = None, None, None, None
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c in (' ', '#'):
                    continue
                point = (x,y)
                if c == '.':
                    self.spaces.add(point)
                    if min_x is None or x < min_x:
                        min_x = x
                    if max_x is None or x > max_x:
                        max_x = x
                    if min_y is None or y < min_y:
                        min_y = y
                    if max_y is None or y > max_y:
                        max_y = y
                else:
                    if point in labels:
                        continue
                    lbl, lpoint, spoint = self.extract_label(point, lines)
                    labels.add(point)
                    labels.add(lpoint)
                    lp = label_points.get(lbl, [])
                    lp.append(spoint)
                    label_points[lbl] = lp
                    self.point_labels[spoint] = lbl
                    if lbl == 'AA':
                        self.start = spoint
                    elif lbl == 'ZZ':
                        self.end = spoint

        # build portal references
        for lp in label_points.values():
            if len(lp) != 2:
                continue
            self.portals[lp[0]] = lp[1]
            self.portals[lp[1]] = lp[0]
            if lp[0][0] in [min_x, max_x] or lp[0][1] in [min_y, max_y]:
                self.outer_portals.add(lp[0])
            else:
                self.outer_portals.add(lp[1])

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

    def routes(self) -> dict[str,list[tuple[Point,int]]]:
        """compute all the possible routes between different portal labels"""
        if self.routes_cache is not None:
            return self.routes_cache
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
        self.routes_cache = r
        return r

    def portal_jump(self, level, point) -> LevelPoint:
        """adjust the portal and level appropriately"""
        if self.recursive:
            if point in self.outer_portals:
                level -= 1
            else:
                level += 1
        return (level, self.portals[point])

    def moves_from(self, level, point) -> list[tuple[Point,int]]:
        """moves to take from the supplied point on the supplied level"""
        points = self.routes()[point]
        if self.recursive:
            moves = []
            for move in points:
                if level == 0 and move[0] in self.outer_portals:
                    continue
                if level != 0 and move[0] in [self.start, self.end]:
                    continue
                moves.append(move)
            points = moves
        return points

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

def best_route(lp: LevelPoint, goal: LevelPoint, visited: set[LevelPoint], maze: Maze) -> int:
    """find the best route between to the goal"""
    if lp == goal:
        return 0
    level, point = lp
    padjust = 0
    if point in maze.portals:
        padjust = 1 # cost of using a portal
        level, point = maze.portal_jump(level, point)
    # made this variable since it seems it required tweaking per puzzle
    # to efficiently complete.  i am sure there is a trick to deal with
    # this more universally, but just going with it for now.
    if level > maze.max_recurse:
        return None
    best = None
    for p, cost in maze.moves_from(level, point):
        nlp = (level,p)
        if nlp in visited:
            continue
        cost += padjust
        nvisited = set(visited)
        nvisited.add(nlp)
        ccost = best_route(nlp, goal, nvisited, maze)
        if ccost is None:
            continue
        if best is None or cost + ccost < best:
            best = cost + ccost
    return best

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
sample3 = """             Z L X W       C                 
             Z P Q B       K                 
  ###########.#.#.#.#######.###############  
  #...#.......#.#.......#.#.......#.#.#...#  
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  
  #.#...#.#.#...#.#.#...#...#...#.#.......#  
  #.###.#######.###.###.#.###.###.#.#######  
  #...#.......#.#...#...#.............#...#  
  #.#########.#######.#.#######.#######.###  
  #...#.#    F       R I       Z    #.#.#.#  
  #.###.#    D       E C       H    #.#.#.#  
  #.#...#                           #...#.#  
  #.###.#                           #.###.#  
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#  
CJ......#                           #.....#  
  #######                           #######  
  #.#....CK                         #......IC
  #.###.#                           #.###.#  
  #.....#                           #...#.#  
  ###.###                           #.#.#.#  
XF....#.#                         RF..#.#.#  
  #####.#                           #######  
  #......CJ                       NM..#...#  
  ###.#.#                           #.###.#  
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#  
  #.....#        F   Q       P      #.#.#.#  
  ###.###########.###.#######.#########.###  
  #.....#...#.....#.......#...#.....#.#...#  
  #####.#.###.#######.#######.###.###.#.#.#  
  #.......#.......#.#.#.#.#...#...#...#.#.#  
  #####.###.#####.#.#.#.#.###.###.#.###.###  
  #.......#.....#.#...#...............#...#  
  #############.#.#.###.###################  
               A O F   N                     
               A A D   M                     """.splitlines()

# Part 1
assert solve_part1(sample) == 23
assert solve_part1(sample2) == 58
assert solve_part1(data) == 658

# Part 2
assert solve_part2(sample, 10) == 26
assert solve_part2(sample3, 15) == 396
assert solve_part2(data, 25) == 7612
