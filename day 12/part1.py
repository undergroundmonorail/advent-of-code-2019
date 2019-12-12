import itertools

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

moons = []

with open('input.txt') as f:
	for line in f:
		moons.append(Moon(*(int(coord.split('=')[1]) for coord in line.strip()[1:-1].split(', '))))

for step in range(1000):
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

print(sum(m.total() for m in moons))