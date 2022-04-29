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
		minDepth = 2,
		initializationMaxTreeDepth = 6,
		maxTreeSize = 10,
		tournamentSize = 4, 
		useLinearScaling = True, 
		reproductionSize = 200,
		fitnessType = 'mse',
		errorEpsilon = 1e-10,
		verbose = False,
		useSSC = False,
		sscLBSS = 1e-4,
		sscUBSS = 0.4,
		sscMaxTrials = 10):
		
		args, _, _, values = inspect.getargvalues(inspect.currentframe())
		values.pop('self')
		for arg, val in values.items():
			setattr(self, arg, val)


	def fit(self, X, y):

		self.X_ = X
		self.y_ = y

		self.fitnessFunction = FitnessFunction(X, y, self.fitnessType)
			
		terminals = []
		nFeatures = X.shape[1]
		for i in range(nFeatures):
			terminals.append(VariableNode(i))

		gp = GP(self.fitnessFunction, self.functions, terminals, 
			populationSize = self.populationSize, 
			maxGenerations = self.maxGenerations,
			maxTime = self.maxTime,
			maxEvaluations = self.maxEvaluations,
			mutationRate = self.mutationRate,
			minDepth = self.minDepth,	
			initializationMaxTreeDepth = self.initializationMaxTreeDepth,
			maxTreeSize = self.maxTreeSize,
			tournamentSize = self.tournamentSize,
			reproductionSize = self.reproductionSize,
			fitnessType = self.fitnessType,
			errorEpsilon = self.errorEpsilon,
			verbose = self.verbose,
			useSSC = self.useSSC,
			sscLBSS = self.sscLBSS,
			sscUBSS = self.sscUBSS,
			sscMaxTrials = self.sscMaxTrials)

		gp.run()
		self.gp = gp
		return self



	def getBest(self):
		return self.gp.fitnessFunction.bestIndividual


	def predict(self, X):
		prediction = self.gp.fitnessFunction.bestIndividual.value(X)
		return prediction