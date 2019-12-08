def chunks(data, n):
	for i in range(0, len(data), n):
		yield data[i:i+n]

image = [' ']*(25*6)

with open('input.txt') as f:
	for layer in reversed(list(chunks(f.read().strip(), 25*6))):
		for n, pixel in (enumerate(layer)):
			if pixel != '2':
				image[n] = pixel

print('\n'.join(''.join(row) for row in chunks(image, 25)).replace('0', ' ').replace('1', '█'))