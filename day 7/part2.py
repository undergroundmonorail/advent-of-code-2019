import itertools

from intcode import *
		
def run_all_until_halted(amps):
	signal = 0
	while not amps[0].halted:
		for amp in amps:
			amp.queue.append(signal)
			amp.run_until_input()
			signal = amp.result.pop(0)
	return signal

with open('input.txt') as f:
	memory = tuple(int(i) for i in f.read().split(','))

def all_inputs():
	for phases in itertools.permutations(range(5, 10)):
		amps = tuple(Intcode(memory, [phase], []) for phase in phases)
		yield run_all_until_halted(amps)

print(max(all_inputs()))