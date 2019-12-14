import collections

from intcode import *

class Arcade(Intcode):
	def __init__(self, memory, queue=None, result=None):
		if queue is None:
			queue = []
		if result is None:
			result = []
		
		super().__init__(memory, queue, result)
		
		self.screen = collections.defaultdict(int)
		self.score = 0
	
	def run(self, debug=False):
		while not self.halted:
			super().step(debug)
			if len(self.result) == 3:
				x, y, tile_id = self.result
				self.result = []
				
				self.screen[(x, y)] = tile_id

with open('input.txt') as f:
	a = Arcade((int(i) for i in f.read().split(',')))

a.run()

print(sum(1 for id in filter(lambda id: id == 2, a.screen.values())))