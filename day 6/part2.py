import sys
sys.setrecursionlimit(9999)

class Body():
	def __init__(self, name):
		self.name = name
		self.parent = None
		self.children = []
	
	def traverse(self, n=0):
		if not self.children:
			return n
		
		return n + sum((o.traverse(n+1) for o in self.children))
	
	def flip(self, new_parent=None):
		if self.parent is not None:
			self.parent.flip(self)
			self.children.append(self.parent)
		
		self.parent = new_parent
		if new_parent in self.children:
			self.children.remove(new_parent)
	
	def distance(self, target, depth=0):
		if self is target:
			return depth
		return min((c.distance(target, depth+1) for c in self.children), default=float('inf'))
	
	def __str__(self, level=0):
		ret = ' '*level + self.name + '\n'
		for o in self.children:
			ret += o.__str__(level + 1)
		return ret

bodies = {'COM' : Body('COM')}

with open('input.txt') as f:
	for line in f:
		name = line.strip().split(')')[1]
		bodies[name] = Body(name)

	f.seek(0)
	
	for line in f:
		orbited, orbiter = line.strip().split(')')		
		bodies[orbited].children.append(bodies[orbiter])
		bodies[orbiter].parent = bodies[orbited]

bodies['YOU'].flip()
print(bodies['YOU'].children[0].distance(bodies['SAN'].parent))