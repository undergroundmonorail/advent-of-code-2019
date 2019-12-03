def add_coords(c1, c2):
	return tuple(a + b for a, b in zip(c1, c2))

def trace(grid, instructions, expected_length):
	current = (0, 0)
	total_length = 0
	for i in instructions:
		direction = {'U':(0,1), 'R':(1,0), 'D':(0,-1), 'L':(-1, 0)}[i[0]]
		length = int(i[1:])
		
		for l in range(length):
			current = add_coords(current, direction)
			total_length += 1
			if len(my_value := grid.get(current, [])) == expected_length:
				grid[current] = my_value + [total_length]
	
	return grid

grid = {}

with open('input.txt') as f:
	wire1 = f.readline()[:-1].split(',')
	wire2 = f.readline()[:-1].split(',')

grid = trace(grid,wire1,0)
grid = trace(grid,wire2,1)

print(min((sum(v) for k,v in grid.items() if len(v)==2)))