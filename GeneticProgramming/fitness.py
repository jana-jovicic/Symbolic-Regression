import numpy as np
from copy import deepcopy

def mse(y_real, y_pred):
	return np.mean(np.square(y_real - y_pred))

def rmse(y_real, y_pred):
	return np.sqrt(np.mean(np.square(y_real - y_pred)))

def nrmse(y_real, y_pred):
	return np.sqrt(np.mean(np.square(y_real - y_pred))) / (np.max(y_real) - np.min(y_real))

def rawFitness(y_real, y_pred):
	return np.sum(np.abs(y_real - y_pred))

def adjustedFitness(y_real, y_pred):
	standardizedFitness = rawFitness(y_real, y_pred) # because this is minimization problem
	return 1 / (1 + standardizedFitness)

def normalizedAdjustedFitness(y_real, y_pred, sumAdjustedFitnesses):
	return adjustedFitness(y_real, y_pred) / sumAdjustedFitnesses

class FitnessFunction:

	def __init__(self, X_train, y_train, fitnessType):
		self.X_train = X_train
		self.y_train = y_train
		self.fitnessType = fitnessType
		self.bestIndividual = None
		self.evaluations = 0
		self.sumAdjustedFitnesses = 0

	def evaluate(self, individual):

		self.evaluations = self.evaluations + 1

		output = individual.value(self.X_train)
		#print("output", output)
		#print("self.y_train", self.y_train)

		fit = np.inf

		if self.fitnessType == 'mse':
			fit = mse(self.y_train, output)
		elif self.fitnessType == 'rmse':
			fit = rmse(self.y_train, output)
		elif self.fitnessType == 'nrmse':
			fit = nrmse(self.y_train, output)
		elif self.fitnessType == 'raw':
			fit = rawFitness(self.y_train, output)
		elif self.fitnessType == 'adjusted':
			fit = adjustedFitness(self.y_train, output)
		elif self.fitnessType == 'normalizedAdjusted':
			fit = normalizedAdjustedFitness(self.y_train, output, self.sumAdjustedFitnesses)


		#print("fit", fit)

		if np.isnan(fit):
			if self.fitnessType == 'adjusted' or self.fitnessType == 'normalizedAdjusted':
				fit = 0
			else:
				fit = np.inf

		print("fit", fit)

		individual.fitness = fit

		if self.fitnessType == 'adjusted' or self.fitnessType == 'normalizedAdjusted':
			updateBestIndividual = not self.bestIndividual or individual.fitness > self.bestIndividual.fitness
		else:
			updateBestIndividual = not self.bestIndividual or individual.fitness < self.bestIndividual.fitness

		if updateBestIndividual:
			del self.bestIndividual
			self.bestIndividual = deepcopy(individual)
