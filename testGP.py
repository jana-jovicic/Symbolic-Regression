import argparse
from tokenize import Double
import numpy as np 
import sklearn.datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import scale
from copy import deepcopy

from expression import *
from GeneticProgramming.GP import GP
from GeneticProgramming.GPEstimator import GeneticProgrammingSymbolicRegressionEstimator
from util.yamlParser import getConfig

np.random.seed(42)

functionNames = {"add": AddNode(), "sub": SubNode(), "mul": MulNode(), "div": DivNode(), "pow": PowNode(), "log": LogNode(), "exp": ExpNode(), "sin": SinNode(), "cos": CosNode()}

def loadDataset(datapointsFile):
	X, y = [], []
	
	with open(datapointsFile, 'r') as file:
		lines = file.readlines()
		for line in lines:
			line = line.split(' ')
			#print(line[:-1])
			xs = [float(x) for x in line[:-1]]
			X.append(xs)
			y.append(float(line[-1]))
	return np.array(X), np.array(y)
		


def main():

	"""
	# Load regression dataset 
	X, y = sklearn.datasets.load_boston( return_X_y=True )
	print(X[:5])
	print(y[:5])

	# Take a dataset split
	X_train, X_test, y_train, y_test = train_test_split( X, y, test_size=0.5, random_state=42 )

	X_train = X_train[:5]
	y_train = y_train[:5]
	X_test = X_test[:5]
	y_test = y_test[:5]

	print(X_train)
	print(y_train)
	"""

	parser = argparse.ArgumentParser(description='GP')
	parser.add_argument("--config", type=str, default='./configs/gp.yaml', help='path to configuration file')
	parser.add_argument('--datapointsFile', default='generatedDatasets/f1.txt', type=str, help='path to file that contains datapoints')
	args = parser.parse_args()

	cfg = getConfig(args.config)
	print(cfg)

	fs = [functionNames[f] for f in cfg['FUNCTIONS']]
	print(fs)

	# Initalize GP estimator
	gpEstimator = GeneticProgrammingSymbolicRegressionEstimator(populationSize=cfg['POPULATION_SIZE'], maxGenerations=cfg['MAX_GENERATIONS'], 
		verbose=cfg['VERBOSE'], maxTreeSize=cfg['MAX_TREE_SIZE'], mutationRate=cfg['MUTATION_RATE'], opMutationRate=cfg['OP_MUTATION_RATE'], 
		minHeight=cfg['MIN_HEIGHT'], initializationMaxTreeHeight=cfg['INITIALIZATION_MAX_TREE_HEIGHT'], 
		tournamentSize=cfg['TOURNAMENT_SIZE'], functions = fs)

	X, y = loadDataset(args.datapointsFile)
	print(X[:5])
	print(y[:5])

	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)

	gpEstimator.fit(X_train, y_train)

	# Get final result
	bestIndividual = gpEstimator.getBest()
	bestStr = bestIndividual.stringRepresentation()
	print('Best individual found:', bestStr)

	# Show mean squared error
	print('Train MSE:',np.mean(np.square(y_train - gpEstimator.predict(X_train))))
	print('Test MSE:',np.mean(np.square(y_test - gpEstimator.predict(X_test))))
	


if __name__ == "__main__":
    main()