import numpy as np
from copy import deepcopy

class FitnessFunction:

	def __init__(self, X_train, y_train):
		self.X_train = X_train
		self.y_train = y_train
		self.bestIndividual = None
		self.evaluations = 0

	def evaluate(self, individual):

		self.evaluations = self.evaluations + 1

		output = individual.value(self.X_train)
		#print("output", output)


		mse = np.mean(np.square(self.y_train - output))
		#print("mse", mse)
		if np.isnan(mse):
			mse = np.inf

		individual.fitness = mse

		if not self.bestIndividual or individual.fitness < self.bestIndividual.fitness:
			del self.bestIndividual
			self.bestIndividual = deepcopy(individual)
