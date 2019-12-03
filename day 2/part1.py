import sys

# Opcode implementations

def add(m, pc):
	m[m.get(pc+3, 0)] = m.get(m.get(pc+1, 0), 0) + m.get(m.get(pc+2, 0), 0)
	return m, pc+4
	
def mul(m, pc):
	m[m.get(pc+3, 0)] = m.get(m.get(pc+1, 0), 0) * m.get(m.get(pc+2, 0), 0)
	return m, pc+4

def halt(m, pc):
	print("Program halted at opcode 99.\nAt memory address 0: {}\nMemory dump:\n{}".format(m[0], m))
	sys.exit(0)

def fail(m, pc):
	sys.exit("Tried to call invalid opcode! m[{}] = {}.\n\nMemory dump:\n{}".format(pc, m[pc], m))

def opcode_lookup(i):
	return {
		1: add,
		2: mul,
		99: halt
	}.get(i, fail)

# Init memeory

memory = {}

with open('input.txt') as f:
	for n, i in enumerate(f.read().split(',')):
		memory[n] = int(i)

# as per part 1 instructions

memory[1] = 12
memory[2] = 2

# Registers

program_counter = 0

# Let's-a go

while True:
	memory, program_counter = opcode_lookup(memory.get(program_counter, 0))(memory, program_counter)