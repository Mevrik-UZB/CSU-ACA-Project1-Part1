# Name: Shukhratbek
# Student ID: 230055
# Data: 09/19/2024


# MIPS Simulator Implementation

# Define opcodes and function codes
HALT_OPCODE = 0x3F
NOOP_OPCODE = 0x00
ADD_OPCODE = 0x20
NAND_OPCODE = 0x0C
MULT_OPCODE = 0x18
LW_OPCODE = 0x23
SW_OPCODE = 0x2B
BEQ_OPCODE = 0x04

# Simulated memory and registers
memory = [0] * 1024
registers = [0] * 32

# Instruction execution functions
def halt():
    print("Halting...")
    exit(0)

def noop():
    pass

def add(r1, r2, rd):
    registers[rd] = registers[r1] + registers[r2]

def nand(r1, r2, rd):
    registers[rd] = ~(registers[r1] & registers[r2]) & 0xFFFFFFFF

def mult(r1, r2):
    result = registers[r1] * registers[r2]
    # In a real implementation, this would set HI and LO registers
    print(f"MULT result: {result}")

def lw(rt, offset, base):
    address = registers[base] + offset
    registers[rt] = memory[address]

def sw(rt, offset, base):
    address = registers[base] + offset
    memory[address] = registers[rt]

def beq(rs, rt, offset):
    if registers[rs] == registers[rt]:
        print(f"BEQ: Branching by {offset}")
        # In a real implementation, this would adjust the PC
    else:
        print("BEQ: No branch")

# Main simulation function
def simulate(instructions):
    for instruction in instructions:
        opcode = instruction >> 26
        if opcode == HALT_OPCODE:
            halt()
        elif opcode == NOOP_OPCODE:
            noop()
        elif opcode == ADD_OPCODE:
            rs = (instruction >> 21) & 0x1F
            rt = (instruction >> 16) & 0x1F
            rd = (instruction >> 11) & 0x1F
            add(rs, rt, rd)
        elif opcode == NAND_OPCODE:
            rs = (instruction >> 21) & 0x1F
            rt = (instruction >> 16) & 0x1F
            rd = (instruction >> 11) & 0x1F
            nand(rs, rt, rd)
        elif opcode == MULT_OPCODE:
            rs = (instruction >> 21) & 0x1F
            rt = (instruction >> 16) & 0x1F
            mult(rs, rt)
        elif opcode == LW_OPCODE:
            rt = (instruction >> 16) & 0x1F
            offset = instruction & 0xFFFF
            base = (instruction >> 21) & 0x1F
            lw(rt, offset, base)
        elif opcode == SW_OPCODE:
            rt = (instruction >> 16) & 0x1F
            offset = instruction & 0xFFFF
            base = (instruction >> 21) & 0x1F
            sw(rt, offset, base)
        elif opcode == BEQ_OPCODE:
            rs = (instruction >> 21) & 0x1F
            rt = (instruction >> 16) & 0x1F
            offset = instruction & 0xFFFF
            beq(rs, rt, offset)

# Test cases
def test_halt_noop():
    print("Testing HALT and NOOP")
    instructions = [
        NOOP_OPCODE << 26,
        HALT_OPCODE << 26
    ]
    simulate(instructions)

def test_arithmetic():
    print("Testing ADD, NAND, and MULT")
    # Set initial values in registers
    registers[1] = 5
    registers[2] = 3
    instructions = [
        (ADD_OPCODE << 26) | (1 << 21) | (2 << 16) | (3 << 11),  # ADD $3, $1, $2
        (NAND_OPCODE << 26) | (1 << 21) | (2 << 16) | (4 << 11),  # NAND $4, $1, $2
        (MULT_OPCODE << 26) | (1 << 21) | (2 << 16)  # MULT $1, $2
    ]
    simulate(instructions)
    print(f"ADD result: {registers[3]}")
    print(f"NAND result: {registers[4]}")

def test_memory_operations():
    print("Testing LW and SW")
    # Set up memory
    memory[100] = 42
    registers[1] = 100  # Base address
    instructions = [
        (LW_OPCODE << 26) | (1 << 21) | (2 << 16) | 0,  # LW $2, 0($1)
        (SW_OPCODE << 26) | (1 << 21) | (2 << 16) | 4   # SW $2, 4($1)
    ]
    simulate(instructions)
    print(f"LW result: Register 2 = {registers[2]}")
    print(f"SW result: Memory[104] = {memory[104]}")

def test_beq():
    print("Testing BEQ")
    registers[1] = 10
    registers[2] = 10
    registers[3] = 5
    instructions = [
        (BEQ_OPCODE << 26) | (1 << 21) | (2 << 16) | 100,  # BEQ $1, $2, 100
        (BEQ_OPCODE << 26) | (1 << 21) | (3 << 16) | 100   # BEQ $1, $3, 100
    ]
    simulate(instructions)
    
# Run all tests
if __name__ == "__main__":
    test_halt_noop()
    test_arithmetic()
    test_memory_operations()
    test_beq()