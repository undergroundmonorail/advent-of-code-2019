from intcode import *

with open('input.txt') as f:
	memory = (int(i) for i in f.read().split(','))

i = Intcode(memory, [1])

i.run()