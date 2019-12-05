import intcode

def main():
	with open('input.txt') as f:
		memory = map(int, f.read().split(','))

	i = intcode.Intcode(memory, [5])
	i.run()

if __name__ == '__main__':
	main()