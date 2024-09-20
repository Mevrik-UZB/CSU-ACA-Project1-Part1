# MIPS Simulator with BEQ, ADD, NAND, and MULT Implementation

# Define opcodes and function codes
BEQ_OPCODE = 0x04
ADD_OPCODE = 0x00
ADD_FUNCT = 0x20
NAND_OPCODE = 0x00
NAND_FUNCT = 0x0C
MULT_OPCODE = 0x00
MULT_FUNCT = 0x18

# Simulated memory and registers
memory = [0] * 1024  # Simulated memory (1024 words)
registers = [0] * 32  # 32 registers
pc = 0  # Program counter

# Function for BEQ (Branch if Equal)
def beq(rs, rt, offset):
    global pc
    if registers[rs] == registers[rt]:
        pc += (offset << 2)  # Shift left by 2 to get word offset
        print(f"BEQ: Branch taken to PC = {pc}")
    else:
        print("BEQ: Branch not taken")

# Function for ADD
def add(rs, rt, rd):
    registers[rd] = registers[rs] + registers[rt]
    print(f"ADD: R[{rd}] = R[{rs}] + R[{rt}] = {registers[rd]}")

# Function for NAND
def nand(rs, rt, rd):
    registers[rd] = ~(registers[rs] & registers[rt]) & 0xFFFFFFFF
    print(f"NAND: R[{rd}] = ~(R[{rs}] & R[{rt}]) = {registers[rd]}")

# Function for MULT
def mult(rs, rt):
    result = registers[rs] * registers[rt]
    print(f"MULT: R[{rs}] * R[{rt}] = {result}")

# Main simulation function
def simulate(instructions):
    global pc
    while pc < len(instructions):
        instruction = instructions[pc]
        opcode = instruction >> 26
        
        if opcode == BEQ_OPCODE:
            rs = (instruction >> 21) & 0x1F
            rt = (instruction >> 16) & 0x1F
            offset = instruction & 0xFFFF
            if offset & 0x8000:  # Check if offset is negative
                offset -= 0x10000  # Convert to signed
            beq(rs, rt, offset)
        elif opcode == ADD_OPCODE:
            funct = instruction & 0x3F
            if funct == ADD_FUNCT:
                rs = (instruction >> 21) & 0x1F
                rt = (instruction >> 16) & 0x1F
                rd = (instruction >> 11) & 0x1F
                add(rs, rt, rd)
            elif funct == NAND_FUNCT:
                rs = (instruction >> 21) & 0x1F
                rt = (instruction >> 16) & 0x1F
                rd = (instruction >> 11) & 0x1F
                nand(rs, rt, rd)
            elif funct == MULT_FUNCT:
                rs = (instruction >> 21) & 0x1F
                rt = (instruction >> 16) & 0x1F
                mult(rs, rt)
        
        # Insert NOPs after branch (assuming no hazards)
        if opcode == BEQ_OPCODE:
            print("Inserting NOP after branch")
            pc += 1
        
        pc += 1

# Test cases
def test_instructions():
    print("Testing BEQ, ADD, NAND, and MULT")
    # Set initial values in registers
    registers[1] = 5
    registers[2] = 5
    registers[3] = 10
    
    instructions = [
        (ADD_OPCODE << 26) | (1 << 21) | (2 << 16) | (4 << 11) | ADD_FUNCT,  # ADD $4, $1, $2
        (NAND_OPCODE << 26) | (1 << 21) | (2 << 16) | (5 << 11) | NAND_FUNCT,  # NAND $5, $1, $2
        (MULT_OPCODE << 26) | (1 << 21) | (2 << 16) | MULT_FUNCT,  # MULT $1, $2
        (BEQ_OPCODE << 26) | (1 << 21) | (2 << 16) | 2,  # BEQ $1, $2, 2 (should branch)
        (ADD_OPCODE << 26) | (1 << 21) | (2 << 16) | (6 << 11) | ADD_FUNCT,  # ADD $6, $1, $2 (should be skipped)
        (BEQ_OPCODE << 26) | (1 << 21) | (3 << 16) | 2,  # BEQ $1, $3, 2 (should not branch)
        (ADD_OPCODE << 26) | (1 << 21) | (3 << 16) | (7 << 11) | ADD_FUNCT,  # ADD $7, $1, $3
    ]
    simulate(instructions)
    
    print("\nFinal register states:")
    for i in range(8):
        print(f"R[{i}] = {registers[i]}")

# Run test case
if __name__ == "__main__":
    test_instructions()