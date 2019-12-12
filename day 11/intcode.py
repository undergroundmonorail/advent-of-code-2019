import sys
import collections
from enum import Enum

class Opcode(Enum):
	ADD = 1
	MUL = 2
	IN = 3
	OUT = 4
	TJMP = 5
	FJMP = 6
	LT = 7
	EQUAL = 8
	RBO = 9
	HALT = 99
	INVALID = -1
	
	@classmethod
	def _missing_(cls, value):
		return Opcode.INVALID

class Mode(Enum):
	POSITION = 0
	IMMEDIATE = 1
	RELATIVE = 2

class Instruction():
	def __len__(self):
		return {
		         Opcode.ADD     : 4,
		         Opcode.MUL     : 4,
		         Opcode.IN      : 2,
		         Opcode.OUT     : 2,
		         Opcode.HALT    : 1,
		         Opcode.TJMP    : 3,
		         Opcode.FJMP    : 3,
		         Opcode.LT      : 4,
		         Opcode.EQUAL   : 4,
				 Opcode.RBO     : 2,
		         Opcode.INVALID : 0,
		       }[self.opcode]
	
	def __init__(self, i):
		self.opcode = Opcode(i % 100)
		i //= 100
		self.first_mode = Mode(i % 10)
		i //= 10
		self.second_mode = Mode(i % 10)
		i //= 10
		self.third_mode = Mode(i % 10)

class Intcode():
	def __init__(self, memory, queue=None, result=None):
		self.memory = collections.defaultdict(int, {n : i for (n, i) in enumerate(memory)})
		
		self.queue = queue
		self.result = result
		
		self.ip = 0
		self.relative_base = 0
		self.halted = False
	
	def run(self, debug=False):
		while not self.halted:
			self.step(debug)

	def run_until_input(self, debug=False):
		while not self.halted and (self.queue or Instruction(self.memory[self.ip]).opcode != Opcode.IN):
			self.step(debug)
	
	def step(self, debug=False):
		"""Execute the instruction at the instruction pointer"""
		if debug:
			instruction = Instruction(self.memory[self.ip])
			print(instruction.opcode)
			for i in range(1, len(instruction)):
				print([instruction.first_mode, instruction.second_mode, instruction.third_mode][i-1], self.memory[self.ip+i])
			print()
		
		def get_value(index, mode):
			if mode == Mode.POSITION:
				return self.memory[self.memory[index]]
			if mode == Mode.IMMEDIATE:
				return self.memory[index]
			if mode == Mode.RELATIVE:
				return self.memory[self.memory[index] + self.relative_base]
		
		def put_value(index, mode, value):
			if mode == Mode.POSITION:
				self.memory[index] = value
			if mode == Mode.RELATIVE:
				self.memory[index + self.relative_base] = value
		
		def add(i):
			v1 = get_value(self.ip+1, i.first_mode)
			v2 = get_value(self.ip+2, i.second_mode)
			
			put_value(self.memory[self.ip+3], i.third_mode, v1 + v2)
		
		def mul(i):
			v1 = get_value(self.ip+1, i.first_mode)
			v2 = get_value(self.ip+2, i.second_mode)
			
			put_value(self.memory[self.ip+3], i.third_mode, v1 * v2)
		
		def in_(i): # damn reserved words
			put_value(self.memory[self.ip+1], i.first_mode, self.get_input())
		
		def out(i):
			self.put_output(get_value(self.ip+1, i.first_mode))
		
		def tjmp(i):
			if get_value(self.ip+1, i.first_mode):
				self.ip = get_value(self.ip+2, i.second_mode)
				self.ip -= len(i) # Offset the increment that will happen next
		
		def fjmp(i):
			if not get_value(self.ip+1, i.first_mode):
				self.ip = get_value(self.ip+2, i.second_mode)
				self.ip -= len(i) # Offset the increment that will happen next
		
		def lt(i):
			put_value(self.memory[self.ip+3], i.third_mode, int(get_value(self.ip+1, i.first_mode) < get_value(self.ip+2, i.second_mode)))
		
		def equal(i):
			put_value(self.memory[self.ip+3], i.third_mode, int(get_value(self.ip+1, i.first_mode) == get_value(self.ip+2, i.second_mode)))
		
		def rbo(i):
			self.relative_base += get_value(self.ip+1, i.first_mode)
		
		def halt(i):
			self.halted = True
		
		def invalid(i):
			sys.exit(("Invalid instruction reached! Tried to execute instruction {} at memory position {}\n\n" +
			          "Memory dump:\n" +
			          "{}").format(self.memory[self.ip], self.ip, self.memory))
		
		curr = Instruction(self.memory[self.ip])
		
		{
		  Opcode.ADD     : add,
		  Opcode.MUL     : mul,
		  Opcode.IN      : in_,
		  Opcode.OUT     : out,
		  Opcode.TJMP    : tjmp,
		  Opcode.FJMP    : fjmp,
		  Opcode.LT      : lt,
		  Opcode.EQUAL   : equal,
		  Opcode.RBO     : rbo,
		  Opcode.HALT    : halt,
		  Opcode.INVALID : invalid,
		}[curr.opcode](curr)
		
		self.ip += len(curr)

	def get_input(self):
		# The queue of inputs ready to enter
		if self.queue:
			return self.queue.pop(0)
		return int(input())

	def put_output(self, i):
		# The queue of outputs ready to be read
		if self.result is not None:
			self.result.append(i)
		else:
			print(i)