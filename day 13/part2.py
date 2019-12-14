import collections
from intcode import *
cmp=lambda a,b:(a>b)-(a<b)

class Arcade(Intcode):
	def __init__(self, memory, queue=None, result=None):
		if queue is None:
			queue = []
		if result is None:
			result = []
		
		super().__init__(memory, queue, result)
		
		self.screen = collections.defaultdict(int)
		self.score = 0
		
		self.ball_x = 0
		self.paddle_x = 0
	
	def step(self, debug=False):
		super().step(debug)
		if len(self.result) == 3:
			x, y, tile_id = self.result
			self.result = []
			
			if (x, y) == (-1, 0):
				self.score = tile_id
			else:
				self.screen[(x, y)] = tile_id
				if tile_id == 3:
					self.paddle_x = x
				elif tile_id == 4:
					self.ball_x = x
	
	def cheat(self, display=False, debug=False):
		while not self.halted:
			self.run_until_input()
			self.queue.append(cmp(self.ball_x, self.paddle_x))
			if display:
				self.display()
	
	def display(self, palette=None):
		print('\033[H')
		print(self.score)
		
		if palette is None:
			palette = {0: '  ', 1: '##', 2: '[]', 3: '--', 4: '()'}
		
		max_x = max((coord[0] for coord in self.screen.keys()))
		max_y = max((coord[1] for coord in self.screen.keys()))
		
		for y in range(max_y + 1):
			for x in range(max_x + 1):
				print(palette[self.screen[(x, y)]], end='')
			print()

with open('input.txt') as f:
	a = Arcade((int(i) for i in f.read().split(',')))

a.memory[0] = 2 # play without quarters
a.cheat()
print(a.score)