import intcode

def main():
	with open('input.txt') as f:
		memory = map(int, f.read().split(','))

	i = intcode.Intcode(memory, [1], [])
	i.run()
	print(i.result[-1])

if __name__ == '__main__':
	main()