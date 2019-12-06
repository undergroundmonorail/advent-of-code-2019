class Body():
	def __init__(self, name):
		self.name = name
		self.orbiters = []
	
	def traverse(self, n=0):
		if not self.orbiters:
			return n
		
		return n + sum((o.traverse(n+1) for o in self.orbiters))

bodies = {'COM' : Body('COM')}

with open('input.txt') as f:
	for line in f:
		name = line.strip().split(')')[1]
		bodies[name] = Body(name)

	f.seek(0)
	
	for line in f:
		orbited, orbiter = line.strip().split(')')
		bodies[orbited].orbiters.append(bodies[orbiter])

print(bodies['COM'].traverse())