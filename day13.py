"""utility imports"""
from utilities.data import read_lines, parse_integers
from utilities.runner import runner

@runner("Day 13", "Part 1")
def solve_part1(line: str):
    """part 1 solving function"""
    oc = parse_integers(line, ",")
    game = Game()
    computer = Computer(oc, game)
    computer.run()
    return game.tiles

@runner("Day 13", "Part 2")
def solve_part2(line: str):
    """part 2 solving function"""
    oc = parse_integers(line, ",")
    oc[0] = 2
    game = Game()
    computer = Computer(oc, game)
    computer.run()
    return game.score

class Game:
    """structure for painting robot"""
    def __init__(self):
        self.tiles = 0
        self.score = 0
        self.output = []
        self.paddle = (0,0)
        self.ball = (0,0)
        self.moving = 1

    def provide_input(self):
        """
        provide joystick input. determine x location the ball will be at when
        it reaches the paddle Y location based on which way it is currently moving
        and then provide the joystick input to move the paddle to the appropriate
        X location.
        """
        steps_to_bounce = abs(self.paddle[1]-self.ball[1]) - 1
        bounce_x_loc = self.ball[0] + (steps_to_bounce * self.moving)
        paddle_x = self.paddle[0]
        if paddle_x < bounce_x_loc:
            return 1
        if paddle_x > bounce_x_loc:
            return -1
        return 0

    def accept_output(self, o: int):
        """accept output value and perform robot actions accordingly"""
        self.output.append(o)
        if len(self.output) % 3 == 0:
            if self.output[-3] == -1 and self.output[-2] == 0:
                self.score = self.output[-1]
                return
            if self.output[-1] == 2:
                self.tiles += 1
            if self.output[-1] == 4:
                ball_loc = (self.output[-3], self.output[-2])
                #print(f"ball is at position: {ball_loc}")
                self.moving = 1 if ball_loc[0] > self.ball[0] else -1
                self.ball = ball_loc
            if self.output[-1] == 3:
                self.paddle = (self.output[-3], self.output[-2])
                #print(f"paddle is at position: {self.paddle}")

class Computer:
    """structure for computer"""
    def __init__(self, op: list[int], game: Game):
        self.op = {i:o for i, o in enumerate(op)}
        self.game = game
        self.opi = 0
        self.relative_base = 0
        self.done = False

    def run(self) -> bool:
        """run the intcode program and return value"""
        i = self.opi
        while i < len(self.op):
            opcode, m1, m2, m3 = self.opcode_modes(self.opc(i))
            if opcode == 99:
                self.done = True
                break
            if opcode == 1:
                self.op[self.pvi(i+3,m3)] = self.pv(i+1,m1) + self.pv(i+2,m2)
                i += 4
            elif opcode == 2:
                self.op[self.pvi(i+3,m3)] = self.pv(i+1,m1) * self.pv(i+2,m2)
                i += 4
            elif opcode == 3:
                self.op[self.pvi(i+1,m1)] = self.game.provide_input()
                i += 2
            elif opcode == 4:
                self.game.accept_output(self.pv(i+1,m1))
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
data = read_lines("input/day13/input.txt")[0]

# Part 1
assert solve_part1(data) == 357

# Part 2
assert solve_part2(data) == 17468
