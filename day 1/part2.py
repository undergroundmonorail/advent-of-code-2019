def fuel_calc(mass):
	return max(mass//3-2, 0)

def fuel_for_module(mass):
	fuel_running = fuel_calc(int(mass))
	additional_fuel = fuel_calc(fuel_running)
	
	while (new_fuel := fuel_calc(additional_fuel)):
		fuel_running += additional_fuel
		additional_fuel = new_fuel
	
	return fuel_running + additional_fuel

with open('input.txt') as f:
	print(sum(map(fuel_for_module, f.read().split())))