from Bee import Bee
import random
import sys
import copy

class BeeHive(object):
	
	def __init__(	self,
					lower,
					upper,
					evalFunc		= None,
					numBees			= 50,
					totalIteration	= 100,
					maximumTrial	= None,
					selectFunc		= None,
					seed			= None,
					verbose			= False,
					otherParams		= None):
		
		
		#size upper sama lower harus sama
		assert(len(upper) == len(lower))

		
		#properties
		self.lower			= lower
		self.upper			= upper
		self.evalFunc		= evalFunc
		self.numBees 		= int((numBees + numBees % 2)) #kenapa harus genap ?
		self.dimension		= len(lower)
		self.totalIteration = totalIteration
		self.selectFunc 	= selectFunc
		self.verbose		= verbose
		self.otherParams 	= otherParams
		
		if(seed == None):
			self.seed = random.randint(0, 1000) #kenapa 0-1000 ?
		else:
			self.seed = seed
		random.seed(self.seed) #?

		if(maximumTrial == None):
			self.maximumTrial = 0.6 * self.numBees * self.dimension #kenapa begini ?
		else
			self.maximumTrial = maximumTrial

		#inisialisasi solusi terbaik
		self.best 			= sys.float_info.max
		self.solution 		= None

		#bikin populasi lebah
		self.population 	= [Bee(lower,upper,evalFunc) for i in range(self.numBees)]

		#inisialisasi lokasi nektar terbaik
		self.findBest()

		#menghitung kemungkinan nektar tersebut terpilih
		self.calcProbability()


	def findBest(self):
		#mencari posisi lebah terbaik
		values 	= [bee.value for bee in self.population]
		index	= values.index(min(values))
		if(values[index] < self.best):
			self.best 		= values[index]
			self.solution 	= self.population[index].vector

	def calcProbability(self):
		#menghitung kemungkinan solusi yg dipilih oleh onlooker bee 
		#setelah tarian yang diberikan oleh employeed bee sebelum kembali ke sarang
		
		#fitness dari lebah2 yg ada di sarang
		values 		= [bee.fitness for bee in self.population]
		maxValues 	= max(values)

		#menghitung probabilitas
		if(self.selectFunc == None):
			self.prob = [0.9 * v / maxvalues + 0.1 for v in values]
		else:
			if(self.otherParams != None):
				self.prob = self.selectFunc(list(values), **self.otherParams)
			else:
				self.prob = self.selectFunc(values)

		return [sum(self.prob[:i+1]) for i in range(self.size)]

	def run(self):
		cost 		 = {}
		cost["best"] = []
		cost["mean"] = []

		for i in range(self.totalIteration):
			
			#employees bee
			for idx in range(self.size):
				self.sendEmployee(idx)

			#onlookers bee
			self.sendOnlookers()

			#scout bee
			self.sendScout()

			#menghitung best path
			self.findBest()

			#stores convergence information
			cost["best"].append(self.best)
			cost["mean"].append(sum([bee.value for bee in self.population]) / self.size )

			#print information
			if self.verbose:
				self.verbose(i,cost)

	def sendEmployee(self, currIdx):
		#meniru lebah yg sekarang
		beeClone = copy.deepcopy(self.population[currIdx])

		#dimensi
		dim = random.randint(0, self.dim-1)

		#memilih lebah lain
		otherIdx = currIdx
		while(otherIdx == currIdx): otherIdx = random.randint(0, self.size-1)

		#membuat tiruan kumpulan lebah
		beeClone.vector[dim] = self.clone(dim, currIdx, otherIdx)

		#cek batasan
		beeClone.vector = self.check(beeClone.vector, dim=dim)

		#menghitung fitness lebah tiruan
		beeClone.value = self.evalFunc(beeClone.vector)
		beeClone.fitness()

		#memilih lebah terbaik
		if (beeClone.fitness > self.population[currIdx].fitness):
			self.population[currIdx] = copy.deepcopy(beeClone)
			self.population[currIdx].counter = 0
		else:
			self.population[currIdx].counter += 1

	def sendOnlookers(self):
		onlookersBee = 0
		beta = 0

		while (onlookersBee < self.size):
			phi = random.random()

			beta += phi * max(self.prob)
			beta %= max(self.prob)

			#pilih & kirim lebah onlooker baru
			index = self.select(beta)
			self.sendEmployee(index)

			onlookersBee += 1

	def select(self, beta):
		prob = self.calcProbability()

		for i in range(self.size):
			if(beta < prob[i]):
				return i

	def sendScout(self):
		trial = [self.population[i].counter for i in range(self.size)]

		#identifikasi lebah dengan percobaan paling banyak
		idx = trial.index(max(trial))

		#jika jumlah percobaan melebihi dari batas trial maximum yg sudah ditentukan
		if(trial[index] > self.maximumTrial)
			self.population[idx] = Bee(self.lower, self.upper, self.evaluate)
			self.sendEmployee(idx)

	def clone(self, dim, currIdx, otherIdx):
		return self.population[currIdx].vector[dim] + \
				(random.random() - 0.5) * 2			* \
				(self.population[currIdx].vector[dim] - self.population[otherIdx].vector[dim])

	def check(self, vector, dim = None):
		if(dim == None):
			range = range(self.dim)
		else:
			range = [dim]

		for i in range:
			if(vector[i] < self.lower[i]):
				vector[i] = self.lower[i]
			elif(vector[i] > self.upper[i]):
				vector[i] = self.upper[i]

		return vector

	def verbose(self, i, cost):
		msg = "# Iter = {} | Best Evaluation Value = {} | Mean Evaluation Value = {}"
		print(msg.format(int(itr), cost["best"][itr], cost["mean"][itr])
