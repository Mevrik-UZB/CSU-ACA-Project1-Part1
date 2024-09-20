# MIPS Simulator with LW and SW Implementation

# Define opcodes
LW_OPCODE = 0x23
SW_OPCODE = 0x2B

# Simulated memory and registers
memory = [0] * 1024  # Simulated memory (1024 words)
registers = [0] * 32  # 32 registers

# Function for LW (Load Word)
def lw(rt, offset, base):
    address = registers[base] + offset
    if 0 <= address < len(memory):
        registers[rt] = memory[address]
        print(f"LW: R[{rt}] = Memory[{address}] = {registers[rt]}")
    else:
        print(f"LW: Invalid memory address {address}")

# Function for SW (Store Word)
def sw(rt, offset, base):
    address = registers[base] + offset
    if 0 <= address < len(memory):
        memory[address] = registers[rt]
        print(f"SW: Memory[{address}] = R[{rt}] = {registers[rt]}")
    else:
        print(f"SW: Invalid memory address {address}")

# Main simulation function
def simulate(instructions):
    for instruction in instructions:
        opcode = instruction >> 26
        if opcode == LW_OPCODE:
            rt = (instruction >> 16) & 0x1F
            base = (instruction >> 21) & 0x1F
            offset = instruction & 0xFFFF
            if offset & 0x8000:  # Check if offset is negative
                offset -= 0x10000  # Convert to signed
            lw(rt, offset, base)
        elif opcode == SW_OPCODE:
            rt = (instruction >> 16) & 0x1F
            base = (instruction >> 21) & 0x1F
            offset = instruction & 0xFFFF
            if offset & 0x8000:  # Check if offset is negative
                offset -= 0x10000  # Convert to signed
            sw(rt, offset, base)

# Test cases
def test_lw_sw():
    print("Testing LW and SW")
    # Initialize some memory locations
    memory[100] = 42
    memory[104] = 99
    
    # Set base address in register 1
    registers[1] = 100
    
    instructions = [
        (LW_OPCODE << 26) | (1 << 21) | (2 << 16) | 0,     # LW $2, 0($1)
        (LW_OPCODE << 26) | (1 << 21) | (3 << 16) | 4,     # LW $3, 4($1)
        (SW_OPCODE << 26) | (1 << 21) | (2 << 16) | 8,     # SW $2, 8($1)
        (SW_OPCODE << 26) | (1 << 21) | (3 << 16) | 12,    # SW $3, 12($1)
        (LW_OPCODE << 26) | (1 << 21) | (4 << 16) | 8,     # LW $4, 8($1)
        (LW_OPCODE << 26) | (1 << 21) | (5 << 16) | 12,    # LW $5, 12($1)
    ]
    simulate(instructions)
    
    print("\nFinal state:")
    print(f"R[2] = {registers[2]}")
    print(f"R[3] = {registers[3]}")
    print(f"R[4] = {registers[4]}")
    print(f"R[5] = {registers[5]}")
    print(f"Memory[108] = {memory[108]}")
    print(f"Memory[112] = {memory[112]}")

# Run test case
if __name__ == "__main__":
    test_lw_sw()