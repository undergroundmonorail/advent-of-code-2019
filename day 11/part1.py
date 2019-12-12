import collections
from intcode import *

class Robot():
	def __init__(self, code, direction=(0, 1), coords=(0,0)):
		self.intcode = Intcode(code, [], [])
		self.direction = direction
		self.coords = coords
		
		self.intcode.run_until_input()
	
	def turn_and_move(self, direction):
		# 0 == counterclockwise
		# 1 == clockwise
		
		#              up      right   down     left     up      left
		directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (0, 1), (-1, 0)]
		
		if direction:
			new_direction = directions[directions.index(self.direction)+1]
		else:
			new_direction = directions[directions.index(self.direction)-1]
		
		self.direction = new_direction
		
		self.coords = (self.coords[0] + self.direction[0], self.coords[1] + self.direction[1])
		

with open('input.txt') as f:
	code = [int(i) for i in f.read().split(',')]

my_robot = Robot(code)
hull = collections.defaultdict(int)
painted = set()

while not my_robot.intcode.halted:
	my_robot.intcode.queue.append(hull[my_robot.coords])
	my_robot.intcode.run_until_input()
	
	colour = my_robot.intcode.result.pop(0)
	hull[my_robot.coords] = colour
	painted.add(my_robot.coords)
	
	direction = my_robot.intcode.result.pop(0)
	my_robot.turn_and_move(direction)

print(len(painted))