import itertools

from intcode import *

def run_until_input(i):
	while not i.halted and (i.queue or Instruction(i.memory[i.ip]).opcode != Opcode.IN):
		i.step()
		
def run_all_until_halted(amps):
	signal = 0
	while not amps[0].halted:
		for amp in amps:
			amp.queue.append(signal)
			run_until_input(amp)
			signal = amp.result.pop(0)
	return signal

with open('input.txt') as f:
	memory = tuple(int(i) for i in f.read().split(','))

def all_inputs():
	for phases in itertools.permutations(range(5, 10)):
		a,b,c,d,e = phases
		amps = (Intcode(memory, [a], []), Intcode(memory, [b], []), Intcode(memory, [c], []), Intcode(memory, [d], []), Intcode(memory, [e], []))
		yield run_all_until_halted(amps)

print(max(all_inputs()))