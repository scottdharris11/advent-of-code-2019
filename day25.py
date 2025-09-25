"""utility imports"""
import itertools
import random
import re
from utilities.data import read_lines, parse_integers
from utilities.runner import runner

@runner("Day 25", "Part 1")
def solve_part1(line: str) -> int:
    """part 1 solving function"""
    oc = parse_integers(line, ",")
    io = IOProvider()
    computer = Computer(oc, io)
    computer.run()
    pmatcher = re.compile(r"You should be able to get in by typing ([0-9]+) on the keypad")
    pmatch = pmatcher.findall(io.last_msg)
    if len(pmatch) > 0:
        return int(pmatch[0])
    return -1

def to_ascii_code(line: str) -> list[int]:
    """convert ascii input instructions into intcodes"""
    output = []
    for i in line:
        output.append(ord(i))
    output.append(10)
    return output

def to_ascii(vals: list[int]) -> str:
    """convert output intcodes to string"""
    output = ""
    for val in vals:
        if val > 255:
            continue
        output += chr(val)
    return output

def unique_combinations(items: list[str]):
    """build the set of unique combinations from the supplied items"""
    combos = []
    for size in range(1, len(items)+1):
        sc = itertools.combinations(items, size)
        for c in sc:
            combos.append(list(c))
    return combos

ITEMS_TO_SKIP = {"giant electromagnet", "photons", "molten lava", "escape pod", "infinite loop"}

class IOProvider:
    """structure for robot"""
    def __init__(self):
        self.output_vals = []
        self.items = []
        self.doors = []
        self.items_to_take = []
        self.instructions = []
        self.instructions_idx = 0
        self.listing_items = False
        self.password = None
        self.halt = False
        self.last_msg = None
        self.try_combos = False
        self.holding_items = []
        self.combos = None
        self.current_combo = None
        self.next_combo_idx = 0

    def provide_input(self):
        """provide input to the program"""
        if len(self.instructions) == 0:
            return 0
        instruct = self.instructions[self.instructions_idx]
        self.instructions_idx += 1
        if self.instructions_idx == len(self.instructions):
            self.instructions = []
            self.instructions_idx = 0
        return instruct

    def accept_output(self, o: int):
        """accept output value and record mapping actions accordingly"""
        if o == 10:
            if len(self.output_vals) == 0:
                return
            a = to_ascii(self.output_vals)
            if a.startswith("=="):
                if a == "== Security Checkpoint ==" and len(self.items) == 8:
                    if not self.try_combos:
                        self.try_combos = True
                        self.holding_items.extend(self.items)
            if a == "- north":
                self.doors.append("north")
            if a == "- south":
                self.doors.append("south")
            if a == "- east":
                self.doors.append("east")
            if a == "- west":
                self.doors.append("west")
            if a == "Items here:":
                self.listing_items = True
            if self.listing_items and a.startswith("-"):
                item = a[2:]
                if item not in ITEMS_TO_SKIP:
                    self.items_to_take.append(item)
            if a == "Command?":
                if self.try_combos:
                    # we reached the security checkpoint.  after trial and error
                    # we know there are 8 possible items that could be in our
                    # possession.  once we have all eight, we also know that the
                    # pressure room is just to our south, so we will use different
                    # combinations of the items until we get the right weight
                    if self.combos is None:
                        self.combos = unique_combinations(self.items)
                    if self.current_combo is None:
                        if len(self.holding_items) > 0:
                            # drop items
                            item = self.holding_items.pop()
                            self.instructions = to_ascii_code("drop " + item)
                        else:
                            # activate next combo to check and pickup first item
                            self.current_combo = self.next_combo_idx
                            item = self.combos[self.current_combo][0]
                            self.instructions = to_ascii_code("take " + item)
                            self.holding_items.append(item)
                    else:
                        # keep adding items from combo until all added. once
                        # all added, then move "south" to the room
                        if len(self.holding_items) == len(self.combos[self.current_combo]):
                            #print(f"trying combo: {self.holding_items}")
                            self.instructions = to_ascii_code("south")
                            self.current_combo = None
                            self.next_combo_idx += 1
                        else:
                            item = self.combos[self.current_combo][len(self.holding_items)]
                            self.instructions = to_ascii_code("take " + item)
                            self.holding_items.append(item)
                else:
                    # in exploration mode:
                    #  1. if item available to grab, do it
                    #  2. if no items available, pick a random direction
                    self.listing_items = False
                    if len(self.items_to_take) > 0:
                        item = self.items_to_take.pop()
                        self.items.append(item)
                        self.instructions = to_ascii_code("take " + item)
                    else:
                        direction = self.doors[random.randint(0,len(self.doors)-1)]
                        self.instructions = to_ascii_code(direction)
                        self.doors = []
            self.last_msg = a
            #print(a)
            self.output_vals = []
        else:
            self.output_vals.append(o)

    def halt_program(self) -> bool:
        """exit point to stop program"""
        return self.halt

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
data = read_lines("input/day25/input.txt")[0]

# Part 1
assert solve_part1(data) == 2214608912
