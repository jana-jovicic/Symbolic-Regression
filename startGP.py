import csv
import time
import os, argparse
import numpy as np 
import sklearn.datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import scale
from copy import deepcopy

from sympy import simplify
from sympy.parsing.sympy_parser import parse_expr

from expression import *
from GeneticProgramming.GP import GP
from GeneticProgramming.GPEstimator import GeneticProgrammingSymbolicRegressionEstimator
from GeneticProgramming.fitness import adjustedFitness, mse, normalizedAdjustedFitness, rawFitness, rmse, nrmse
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
	#parser.add_argument("--GPtype", type=str, default='basic', help='type of GP algorithm')
	parser.add_argument("--config", type=str, default='./configs/gp.yaml', help='path to configuration file')
	parser.add_argument('--datapointsFile', default='generatedDatasets/f1.txt', type=str, help='path to file that contains datapoints')
	parser.add_argument('--realEquation', default='generatedDatasets/f1_solution.txt', type=str, help='path to file that contains exact solution')
	args = parser.parse_args()

	cfg = getConfig(args.config)
	print(cfg)

	fs = [functionNames[f] for f in cfg['FUNCTIONS']]
	print(fs)

	errorType = cfg['ERROR_TYPE']

	# Initalize GP estimator


	gpEstimator = GeneticProgrammingSymbolicRegressionEstimator(populationSize=cfg['POPULATION_SIZE'], maxGenerations=cfg['MAX_GENERATIONS'], 
		verbose=cfg['VERBOSE'], maxTreeSize=cfg['MAX_TREE_SIZE'], mutationRate=cfg['MUTATION_RATE'], opMutationRate=cfg['OP_MUTATION_RATE'], 
		minHeight=cfg['MIN_HEIGHT'], initializationMaxTreeHeight=cfg['INITIALIZATION_MAX_TREE_HEIGHT'], 
		tournamentSize=cfg['TOURNAMENT_SIZE'], reproductionSize=cfg['REPODUCTION_SIZE'], 
		errorType=errorType, errorEpsilon=cfg['ERROR_EPSILON'], functions = fs,
		useSSC = cfg['SSC']['USE_SSC'],
		sscLBSS = cfg['SSC']['LBSS'],
		sscUBSS = cfg['SSC']['UBSS'],
		sscMaxTrials = cfg['SSC']['MAX_TRIALS'])

	
	X, y = loadDataset(args.datapointsFile)
	print('Xs', X[:5])
	print('ys', y[:5])

	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

	dir = './GeneticProgramming/results/'

	if cfg['SSC']['USE_SSC']:
		dir += 'SSC'
	else:
		dir += 'basicGP'

	if not os.path.exists(dir):
		os.makedirs(dir)
	resFile = args.datapointsFile[args.datapointsFile.rfind(os.path.sep) : ]
	resFile = dir + resFile
	open(resFile, 'w').close()

	csvFile = resFile[: resFile.rfind('.')] + '.csv'
	open(csvFile, 'w').close()
	header = ['Run', 'TrainError', 'TestError', 'BestIndividual', 'GenerationOfBestSolution', 'Time', 'SympyEquivalence']
	# dodati symbolicEquivalence (pomocu sympy)

	with open(csvFile, 'w', encoding='UTF8') as file:
		writer = csv.writer(file)
		writer.writerow(header)

	with open(resFile, 'a+') as file:
		file.write('Population size: ' + str(cfg['POPULATION_SIZE']) + '\n')
		file.write('Max number of generations: ' + str(cfg['MAX_GENERATIONS']) + '\n')
		file.write('Reproduction size: ' + str(cfg['REPODUCTION_SIZE']) + '\n')
		file.write('Mutation rate: ' + str(cfg['MUTATION_RATE']) + '\n')
		file.write('One point mutation rate: ' + str(cfg['OP_MUTATION_RATE']) + '\n')
		file.write('Error type: ' + str(errorType) + '\n')
		if cfg['SSC']['USE_SSC']:
			file.write('LBSS: ' + str(cfg['SSC']['LBSS']) + '\n')
			file.write('UBSS: ' + str(cfg['SSC']['UBSS']) + '\n')
			file.write('Max trials: ' + str(cfg['SSC']['MAX_TRIALS']) + '\n')



	if args.realEquation:
		with open(args.realEquation) as file:
			realEquationSympy = parse_expr(file.readline())


	for run in range(cfg['NUM_RUNS']):

		startTime = round(time.time())

		gpEstimator.fit(X_train, y_train)

		endTime = round(time.time()) - startTime

		bestIndividual = gpEstimator.getBest()
		bestStr = bestIndividual.stringRepresentation()
		print('Best individual:', bestStr)

		bestIndividualSympy = parse_expr(bestStr)
		equationsDiff = bestIndividualSympy - realEquationSympy
		diffSimplified = simplify(equationsDiff)
		sympyEquivalence = str(diffSimplified == 0)

		y_train_pred = gpEstimator.predict(X_train)
		y_test_pred = gpEstimator.predict(X_test)

		if errorType == 'mse':
			trainErr = mse(y_train, y_train_pred)
			testErr = mse(y_test, y_test_pred)
		elif errorType == 'rmse':
			trainErr = rmse(y_train, y_train_pred)
			testErr = rmse(y_test, y_test_pred)
		elif errorType == 'nrmse':
			trainErr = nrmse(y_train, y_train_pred)
			testErr = nrmse(y_test, y_test_pred)
		elif errorType == 'raw':
			trainErr = rawFitness(y_train, y_train_pred)
			testErr = rawFitness(y_test, y_test_pred)
		elif errorType == 'adjusted':
			trainErr = adjustedFitness(y_train, y_train_pred)
			testErr = adjustedFitness(y_test, y_test_pred)
		elif errorType == 'normalizedAdjusted':
			trainErr = normalizedAdjustedFitness(y_train, y_train_pred, gpEstimator.fitnessFunction.sumAdjustedFitnesses)
			testErr = normalizedAdjustedFitness(y_test, y_test_pred, gpEstimator.fitnessFunction.sumAdjustedFitnesses)

		print('Train' + errorType + ' :', trainErr)
		print('Test' + errorType + ' :', testErr)

		"""
		with open(resFile, 'a+') as file:
			file.write('Run ' + str(run) + ':\n')
			file.write('Best individual: ' + bestStr + '\n')
			file.write('Solution found at generation: ' + str(gpEstimator.gp.generations) + '\n')
			file.write('Train error: ' + str(trainErr) + '\n')
			file.write('Test error: ' + str(testErr) + '\n')
			file.write('-------------------------------\n')
		"""

		generationOfBestSolution = gpEstimator.gp.generations
		data = [run, trainErr, testErr, bestStr, generationOfBestSolution, endTime]
		if args.realEquation:
			data.append(sympyEquivalence)
		with open(csvFile, 'a+', encoding='UTF8') as file:
			writer = csv.writer(file)
			writer.writerow(data)


	print('Results are written to ' + resFile + '\n and' + csvFile)
	
	


if __name__ == "__main__":
    main()