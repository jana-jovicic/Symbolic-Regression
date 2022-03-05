import inspect
from GeneticProgramming.GP import GP
from GeneticProgramming.fitness import FitnessFunction
from sklearn.base import BaseEstimator, RegressorMixin

from expression import *


class GeneticProgrammingSymbolicRegressionEstimator(BaseEstimator, RegressorMixin):

	def __init__(self,
		populationSize = 500, 
		maxGenerations = 100, 
		maxEvaluations = -1,
		maxTime = -1,
		functions = [AddNode(), SubNode(), MulNode(), DivNode()], 
		useErc = True,
		mutationRate = 0.5,
		opMutationRate = 0.0,
		minHeight = 2,
		initializationMaxTreeHeight = 6,
		maxTreeSize = 10,
		tournamentSize =4, 
		useLinearScaling = True, 
		reproductionSize = 200,
		verbose = False):
		
		args, _, _, values = inspect.getargvalues(inspect.currentframe())
		values.pop('self')
		for arg, val in values.items():
			setattr(self, arg, val)


	def fit(self, X, y):

		self.X_ = X
		self.y_ = y

		fitnessFunction = FitnessFunction(X, y)
			
		terminals = []
		nFeatures = X.shape[1]
		for i in range(nFeatures):
			terminals.append(VariableNode(i))

		gp = GP(fitnessFunction, self.functions, terminals, 
			populationSize = self.populationSize, 
			maxGenerations = self.maxGenerations,
			maxTime = self.maxTime,
			maxEvaluations = self.maxEvaluations,
			mutationRate = self.mutationRate,
			minHeight = self.minHeight,	
			initializationMaxTreeHeight = self.initializationMaxTreeHeight,
			maxTreeSize = self.maxTreeSize,
			tournamentSize = self.tournamentSize,
			reproductionSize = self.reproductionSize,
			verbose = self.verbose)

		gp.run()
		self.gp = gp
		return self



	def getBest(self):
		return self.gp.fitnessFunction.elite


	def predict(self, X):
		prediction = self.gp.fitnessFunction.elite.value(X)
		return prediction