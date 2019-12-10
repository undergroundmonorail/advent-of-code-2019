import math
import collections

class Asteroid():
	def __init__(self, coords):
		self.coords = coords

	def relative_to(self, coords):
		if self.coords == coords: return (0, 0)
		return (self.coords[0] - coords[0], self.coords[1] - coords[1])
	
	def direction_from(self, coords):
		if self.coords == coords: return (0, 0)
		return simplify_vector(self.relative_to(coords))
	
	def degrees_from(self, coords):
		if self.coords == coords: return -1
		
		direction = self.direction_from(coords)
		if direction == (0, -1):
			return 0
		if direction == (1, 0):
			return 90
		if direction == (0, 1):
			return 180
		if direction == (-1, 0):
			return 270
		
		quadrant = {(1, -1): 1, (1, 1): 2, (-1, 1): 3, (-1, -1): 4}[(math.copysign(1, direction[0]), math.copysign(1, direction[1]))]
		
		if quadrant in (1, 2):
			return 90 + math.degrees(math.atan(direction[1] / direction[0]))
		if quadrant in (3, 4):
			return 270 + math.degrees(math.atan(direction[1] / direction[0]))
			
		
		return quadrant
	
	def distance_from(self, coords):
		x, y = self.relative_to(coords)
		return math.sqrt(x**2 + y**2)
		
def simplify_vector(coords):
		x, y = coords
		
		hcf = math.gcd(abs(x), abs(y))
		simplified_x = x // hcf
		simplified_y = y // hcf
		
		return (simplified_x, simplified_y)

def visible_from(coords):
	directions = collections.defaultdict(lambda: Asteroid((float('inf'), float('inf'))))
	
	for asteroid in asteroids:
		if asteroid.coords == coords: continue
		directions[asteroid.direction_from(coords)] = min(asteroid, directions[asteroid.direction_from(coords)], key=lambda a:a.distance_from(coords))
	
	return directions.values()

with open('input.txt') as f:
	asteroid_map = f.read().strip()

asteroids = []
for y, row in enumerate(asteroid_map.split()):
	for x, col in enumerate(row):
		if col != '.':
			asteroids.append(Asteroid((x,y)))

station = max(asteroids, key=lambda a:len(visible_from(a.coords)))

exploded = []

while len(exploded) < 200:
	for asteroid in sorted(visible_from(station.coords), key=lambda a: a.degrees_from(station.coords)):
		if asteroid is station: continue
		for i, a in enumerate(asteroids):
			if a is asteroid:
				exploded.append(asteroids.pop(i))
				break

print(exploded[199].coords[0] * 100 + exploded[199].coords[1])