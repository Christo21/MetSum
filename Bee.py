import random
import sys

class Bee(object):
	"""docstring for Bee"""
	def __init__(	self, 
					lower, 
					upper, 
					evalFunc, 
					funcon = None): #constraint
		
		#random solution vector
		self.random(lower,upper)

		#constraint
		if not funcon:
			self.valid = True;
		else
			self.valid = funcon(self.vector)

		#fitness
		if(evalFunc != None):
			self.value = evalFunc(self.vector)
		else:
			self.value = sys.float_info.max

		self.fitness()
		self.counter = 0		
		
	def random(self, lower, upper):
		self.vector = []
		for i in range(len(lower)):
				self.vector.append(lower[i] + random.random() * (upper[i] - lower[i]))

	def fitness(self):
		if(self.value >= 0):
			self.fitness = 1 / (1 + self.value)
		else:
			self.fitness = 1 + abs(self.value)
		