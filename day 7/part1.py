import functools
import itertools

class cache():
	def __init__(self, f):
		self.f = f
		self.c = {}
		functools.update_wrapper(self, f)
	
	def __call__(self, *args):
		if args not in self.c:
			self.c[args] = self.f(*args)
		return self.c[args]

@cache
def amplifier(memory, phase, input_signal):
	i = Intcode(memory, [phase, input_signal], [])
	i.run()
	return i.result[0]

def all_amplifiers(memory, phases):
	signal = 0
	for phase in phases:
		signal = amplifier(memory, phase, signal)
	return signal

with open('input.txt') as f:
	memory = tuple(int(i) for i in f.read().split(','))

print(max(all_amplifiers(memory, phases) for phases in itertools.permutations(range(5))))