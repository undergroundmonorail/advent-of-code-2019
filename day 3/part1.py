def add_coords(c1, c2):
	return tuple(a + b for a, b in zip(c1, c2))

def manhatten(c1, c2):
	return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])

def trace(grid, instructions, character):
	current = (0, 0)
	for i in instructions:
		direction = {'U':(0,1), 'R':(1,0), 'D':(0,-1), 'L':(-1, 0)}[i[0]]
		length = int(i[1:])
		
		for _ in range(length):
			current = add_coords(current, direction)
			grid[current] = grid.get(current, '') + character

grid = {}

with open('input.txt') as f:
	wire1 = f.readline()[:-1].split(',')
	wire2 = f.readline()[:-1].split(',')

grid = trace(grid,wire1,'1')
grid = trace(grid,wire2,'2')

print(min((manhatten(k, (0, 0)) for k, v in grid.items() if v == '12')))