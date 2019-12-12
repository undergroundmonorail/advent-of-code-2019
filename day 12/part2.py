import itertools
import functools
import math

class Moon():
	def __init__(self, x, y, z, dx=0, dy=0, dz=0):
		self.x = x
		self.y = y
		self.z = z
		
		self.dx = dx
		self.dy = dy
		self.dz = dz
	
	def step(self):
		self.x += self.dx
		self.y += self.dy
		self.z += self.dz

	def potential(self):
		return abs(self.x) + abs(self.y) + abs(self.z)
	
	def kinetic(self):
		return abs(self.dx) + abs(self.dy) + abs(self.dz)
	
	def total(self):
		return self.potential() * self.kinetic()

def lcm(*args):
	return functools.reduce(lambda a, b: a * b // math.gcd(a, b), args)

moons = []

with open('input.txt') as f:
	for line in f:
		moons.append(Moon(*(int(coord.split('=')[1]) for coord in line.strip()[1:-1].split(', '))))

cycle_lengths = [0, 0, 0]

initial_state_x = tuple((m.x, m.dx) for m in moons)
initial_state_y = tuple((m.y, m.dy) for m in moons)
initial_state_z = tuple((m.z, m.dz) for m in moons)

for step in itertools.count(0):
	state_x = tuple((m.x, m.dx) for m in moons)
	state_y = tuple((m.y, m.dy) for m in moons)
	state_z = tuple((m.z, m.dz) for m in moons)
	
	if step:
		if state_x == initial_state_x and not cycle_lengths[0]:
			cycle_lengths[0] = step
		if state_y == initial_state_y and not cycle_lengths[1]:
			cycle_lengths[1] = step
		if state_z == initial_state_z and not cycle_lengths[2]:
			cycle_lengths[2] = step
		
	if all(cycle_lengths): break
	
	for m1, m2 in itertools.permutations(moons, 2):
		if m1.x > m2.x:
			m1.dx -= 1
		elif m1.x < m2.x:
			m1.dx += 1
		
		if m1.y > m2.y:
			m1.dy -= 1
		elif m1.y < m2.y:
			m1.dy += 1
		
		if m1.z > m2.z:
			m1.dz -= 1
		elif m1.z < m2.z:
			m1.dz += 1
	
	for m in moons:
		m.step()

print(lcm(*cycle_lengths))