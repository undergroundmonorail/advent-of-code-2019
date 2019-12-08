def layers(data, width, height):
	for i in range(0, len(data), width*height):
		yield data[i:i+(width*height)]

with open('input.txt') as f:
	print((minlayer := min(layers(f.read().strip(), 25, 6), key=lambda l:l.count('0'))).count('1')*minlayer.count('2'))