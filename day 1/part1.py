with open('input.txt') as f:print(sum(map(lambda m:int(m)//3-2, f.read().split())))