"""utility imports"""
import dataclasses
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 22", "Part 1")
def solve_part1(lines: list[str]):
    """part 1 solving function"""
    values = shuffle(lines, 10007)
    return values.index(2019)

@runner("Day 22", "Part 2")
def solve_part2(lines: list[str]):
    """part 2 solving function"""
    return 0

NEW_STACK_INSTRUCT = "deal into new stack"
DEAL_INSTRUCT = "deal with increment "
CUT_INSTRUCT = "cut "

@dataclasses.dataclass
class Card:
    """structure representing a card"""
    def __init__(self, value: int):
        self.value = value
        self.previous = None
        self.next = None

def shuffle(instructions: list[str], size: int) -> list[int]:
    """shuffle a deck of supplied size using instructions"""
    deck = new_deck(new_values(size))
    for instruct in instructions:
        if instruct == NEW_STACK_INSTRUCT:
            deck = new_stack(deck)
        elif instruct.startswith(DEAL_INSTRUCT):
            increment = int(instruct[len(DEAL_INSTRUCT):])
            deck = deal_stack(deck, increment, size)
        elif instruct.startswith(CUT_INSTRUCT):
            point = int(instruct[len(CUT_INSTRUCT):])
            deck = cut_stack(deck, point)
    return deck_values(deck, 1, size)

def new_values(size: int) -> list[int]:
    """build new value set of supplied size"""
    values = [0] * size
    for val in range(size):
        values[val] = val
    return values

def new_deck(values: list[int]) -> Card:
    """build a new deck of supplied size"""
    top = Card(values[0])
    p = top
    for value in values[1:]:
        n = Card(value)
        p.next = n
        n.previous = p
        p = n
    p.next = top
    top.previous = p
    return top

def new_stack(card: Card) -> Card:
    """new stack deal which essentially reverses"""
    p = card # top of deck
    b = card.previous # bottom of deck
    n = b
    while n.value != card.value:
        n.next = n.previous
        n.previous = p
        p = n
        n = p.next
    n.previous = p
    n.next = b
    return b # bottom is new top

def cut_stack(card: Card, point: int) -> Card:
    """cut stack at supplied point"""
    c = card # top of deck
    for _ in range(abs(point)):
        if point < 0:
            c = c.previous
        else:
            c = c.next
    return c # new top of deck

def deal_stack(card: Card, increment: int, size: int) -> Card:
    """deal deck in increment"""
    return new_deck(deck_values(card, increment, size))

def deck_values(card: Card, increment: int, size: int) -> Card:
    """cut stack at supplied point"""
    values = [None] * size
    idx = 0
    values[idx] = card.value
    c = card.next
    while c.value != card.value:
        idx += increment
        if idx >= size:
            idx -= size
        values[idx] = c.value
        c = c.next
    return values

# Data
data = read_lines("input/day22/input.txt")
sample = """deal with increment 7
deal into new stack
deal into new stack""".splitlines()
sample2 = """cut 6
deal with increment 7
deal into new stack""".splitlines()
sample3 = """deal with increment 7
deal with increment 9
cut -2""".splitlines()
sample4 = """deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1""".splitlines()

# Part 1
assert shuffle(sample, 10) == [0, 3, 6, 9, 2, 5, 8, 1, 4, 7]
assert shuffle(sample2, 10) == [3, 0, 7, 4, 1, 8, 5, 2, 9, 6]
assert shuffle(sample3, 10) == [6, 3, 0, 7, 4, 1, 8, 5, 2, 9]
assert shuffle(sample4, 10) == [9, 2, 5, 8, 1, 4, 7, 0, 3, 6]
assert solve_part1(data) == 8502

# Part 2
assert solve_part2(sample2) == 0
assert solve_part2(data) == 0
