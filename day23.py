"""utility imports"""
from typing import Self
from utilities.data import read_lines, parse_integers
from utilities.runner import runner

@runner("Day 23", "Part 1")
def solve_part1(line: str) -> int:
    """part 1 solving function"""
    oc = parse_integers(line, ",")
    nics = {}
    computers = []
    nat = NAT()
    for addr in range(50):
        nics[addr] = IOProvider(addr, nics, nat)
        computers.append(Computer(oc, nics[addr]))
    while True:
        # run one command at a time per computer until done
        for computer in computers:
            if computer.done:
                continue
            computer.run_command()
            if nat.packet is not None:
                return nat.packet[1]

@runner("Day 23", "Part 2")
def solve_part2(line: str) -> int:
    """part 2 solving function"""
    oc = parse_integers(line, ",")
    nics = {}
    computers = []
    nat = NAT()
    for addr in range(50):
        nics[addr] = IOProvider(addr, nics, nat)
        computers.append(Computer(oc, nics[addr]))
    while True:
        # run one command at a time per computer until done
        for computer in computers:
            if computer.done:
                continue
            computer.run_command()
            if nat.idle_state(computers):
                done, duplicate = nat.resume_network(nics)
                if done:
                    return duplicate

class NAT:
    """structure for the NAT"""
    def __init__(self):
        self.packet = None
        self.last = None

    def idle_state(self, computers: list["Computer"]) -> bool:
        """determine if all computers are idle"""
        for computer in computers:
            if computer.io.idle_requests < 50:
                return False
        return True

    def receive_packet(self, x: int, y: int):
        """receive a packate"""
        self.packet = (x, y)

    def resume_network(self, nics: dict[int,"IOProvider"]) -> tuple[bool,int]:
        """resume the network"""
        if self.packet is None:
            return False, 0
        if self.last is not None and self.packet[1] == self.last[1]:
            return True, self.packet[1]
        #print(f"resuming network with {self.packet}")
        nics[0].receive_packet(self.packet[0], self.packet[1])
        self.last = self.packet
        self.packet = None
        return False, 0

class IOProvider:
    """structure for robot"""
    def __init__(self, address: int, nics: dict[int,Self], nat: NAT):
        self.address = address
        self.nics = nics
        self.queue = []
        self.queue.append([address])
        self.packet = None
        self.pidx = None
        self.output_queue = []
        self.idle_requests = 0
        self.sent_255 = None
        self.nat = nat

    def receive_packet(self, x: int, y: int) -> None:
        """receive packet"""
        self.queue.insert(0, [x,y])

    def provide_input(self) -> int:
        """provide input to the program"""
        if self.packet is None and len(self.queue) > 0:
            self.packet = self.queue.pop()
            self.pidx = 0
        if self.packet is None:
            self.idle_requests += 1
            return -1
        self.idle_requests = 0
        p = self.packet[self.pidx]
        self.pidx += 1
        if self.pidx == len(self.packet):
            self.packet = None
            self.pidx = None
        #print(f"sending input on NIC {self.address}: {p}")
        return p

    def accept_output(self, o: int):
        """accept output value and record mapping actions accordingly"""
        self.output_queue.append(o)
        if len(self.output_queue) == 3:
            #print(f"sending output: {self.output_queue}")
            if self.output_queue[0] == 255:
                self.nat.receive_packet(self.output_queue[1], self.output_queue[2])
            elif self.output_queue[0] in self.nics:
                nic = self.nics[self.output_queue[0]]
                nic.receive_packet(self.output_queue[1], self.output_queue[2])
            self.output_queue = []

    def halt_program(self) -> bool:
        """exit point to stop program"""
        return False

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
        while i < len(self.op) and not self.done:
            i = self.run_command()

    def run_command(self) -> int:
        """run next command for program"""
        i = self.opi
        opcode, m1, m2, m3 = self.opcode_modes(self.opc(i))
        if opcode == 99 or self.io.halt_program():
            self.done = True
            return i
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
data = read_lines("input/day23/input.txt")[0]

# Part 1
assert solve_part1(data) == 22074

# Part 2
assert solve_part2(data) == 14257
