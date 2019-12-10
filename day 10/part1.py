import math

with open('input.txt') as f:
	asteriod_map = f.read().strip()

asteroids = []
for y, row in enumerate(asteriod_map.split()):
	for x, col in enumerate(row):
		if col == '#':
			asteroids.append((x,y))

def simplified_asteroids(coords):
	for asteroid in asteroids:
		if asteroid == coords: continue
		
		relative_x, relative_y = asteroid[0] - coords[0], asteroid[1] - coords[1]
		
		hcf = math.gcd(abs(relative_x), abs(relative_y))
		simplified_x = relative_x // hcf
		simplified_y = relative_y // hcf
		
		yield (simplified_x, simplified_y)

def num_visible(coords):
	return len(set(simplified_asteroids(coords)))

def all_visibilities():
	for (x, y) in asteroids:
		yield num_visible((x, y))

print(max(all_visibilities()))