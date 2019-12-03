import sys

# Opcode implementations

def add(m, pc):
	m[m.get(pc+3, 0)] = m.get(m.get(pc+1, 0), 0) + m.get(m.get(pc+2, 0), 0)
	return m, pc+4
	
def mul(m, pc):
	m[m.get(pc+3, 0)] = m.get(m.get(pc+1, 0), 0) * m.get(m.get(pc+2, 0), 0)
	return m, pc+4

def halt(m, pc):
	#print("Program halted at opcode 99.\nAt memory address 0: {}\nMemory dump:\n{}".format(m[0], m))
	return m, pc

def fail(m, pc):
	sys.exit("Tried to call invalid opcode! m[{}] = {}.\n\nMemory dump:\n{}".format(pc, m[pc], m))

def opcode_lookup(i):
	return {
		1: add,
		2: mul,
		99: halt
	}.get(i, fail)

# Init memeory

init_memory = {}

with open('input.txt') as f:
	for n, i in enumerate(f.read().split(',')):
		init_memory[n] = int(i)

# as per part 2 instructions

for noun in range(100):
	for verb in range(100):

		memory = init_memory.copy()

		memory[1] = noun
		memory[2] = verb

		# Registers
	
		program_counter = 0
	
		# Let's-a go
	
		while (opcode := memory.get(program_counter, 0)) in (1, 2, 99):
			memory, program_counter = opcode_lookup(opcode)(memory, program_counter)
			if opcode == 99: break
		
		if memory[0] == 19690720:
			print(noun * 100 + verb)
			break
		
	else:
		continue
	break