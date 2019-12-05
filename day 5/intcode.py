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
	HALT = 99
	INVALID = -1
	
	@classmethod
	def _missing_(cls, value):
		return Opcode.INVALID

class Mode(Enum):
	POSITION = 0
	IMMEDIATE = 1

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
		self.ip = 0
		
		self.queue = queue
		self.result = result
	
	def run(self):
		while Instruction(self.memory[self.ip]).opcode != Opcode.HALT:
			self.step()
	
	def step(self):
		"""Execute the instruction at the instruction pointer"""
		def get_value(index, mode):
			if mode == Mode.POSITION:
				return self.memory[self.memory[index]]
			if mode == Mode.IMMEDIATE:
				return self.memory[index]
		
		def put_value(index, value):
			self.memory[index] = value
		
		def add(i):
			v1 = get_value(self.ip+1, i.first_mode)
			v2 = get_value(self.ip+2, i.second_mode)
			
			put_value(self.memory[self.ip+3], v1 + v2)
		
		def mul(i):
			v1 = get_value(self.ip+1, i.first_mode)
			v2 = get_value(self.ip+2, i.second_mode)
			
			put_value(self.memory[self.ip+3], v1 * v2)
		
		def in_(i): # damn reserved words
			put_value(self.memory[self.ip+1], self.get_input())
		
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
			put_value(self.memory[self.ip+3], int(get_value(self.ip+1, i.first_mode) < get_value(self.ip+2, i.second_mode)))
		
		def equal(i):
			put_value(self.memory[self.ip+3], int(get_value(self.ip+1, i.first_mode) == get_value(self.ip+2, i.second_mode)))
		
		def halt(i):
			# special case this?
			pass
		
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
		  Opcode.HALT    : halt,
		  Opcode.INVALID : invalid,
		}[curr.opcode](curr)
		
		self.ip += len(curr)

	def get_input(self):
		# The queue of inputs ready to enter
		if (queue := self.queue):
			return queue.pop(0)
		return int(input())

	def put_output(self, i):
		# The queue of outputs ready to be read
		if (result := self.result) is not None:
			result.append(i)
		else:
			print(i)