import csv
import time
import os, argparse
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import scale
from copy import deepcopy

from sympy import simplify
from sympy.parsing.sympy_parser import parse_expr

from expression import *
from GeneticProgramming.GP import GP
from GeneticProgramming.GPEstimator import GeneticProgrammingSymbolicRegressionEstimator
from GeneticProgramming.fitness import mse, r2Score, rmse, nrmse
from util.loadDatasets import loadGeneratedDataset, loadYachtDataset
from util.yamlParser import getConfig

np.random.seed(42)

functionNames = {"add": AddNode(), "sub": SubNode(), "mul": MulNode(), "div": DivNode(), "pow": PowNode(), "log": LogNode(), "exp": ExpNode(), "sin": SinNode(), "cos": CosNode()}


def main():


	parser = argparse.ArgumentParser(description='GP')
	parser.add_argument("--datasetType", type=str, default='generated', help='type of dataset (could be: "generated", "yacht")')
	parser.add_argument("--standardizeData", default=False, action='store_true', help='flag to indicate whether or not to standardize data')
	parser.add_argument("--config", type=str, default='./configs/gp.yaml', help='path to configuration file')
	parser.add_argument('--datapointsFile', required=False, default='generatedDatasets/f1.txt', type=str, help='path to file that contains datapoints')
	parser.add_argument('--realEquation', required=False, default='generatedDatasets/f1_solution.txt', type=str, help='path to file that contains exact solution')
	args = parser.parse_args()

	if args.datasetType == "generated" and args.datapointsFile is None:
		parser.error('\t\t File fith datapoints must be provided. Example usage is in file startGP.sh')

	cfg = getConfig(args.config)
	print(cfg)

	fs = [functionNames[f] for f in cfg['FUNCTIONS']]
	print(fs)

	errorType = cfg['ERROR_TYPE']
	fitnessType = cfg['FITNESS_TYPE']


	gpEstimator = GeneticProgrammingSymbolicRegressionEstimator(populationSize=cfg['POPULATION_SIZE'], maxGenerations=cfg['MAX_GENERATIONS'],
		maxTime=cfg['MAX_HOURS'], maxEvaluations=cfg['MAX_EVALUATIONS'], verbose=cfg['VERBOSE'], 
		maxTreeSize=cfg['MAX_TREE_SIZE'], mutationRate=cfg['MUTATION_RATE'], opMutationRate=cfg['OP_MUTATION_RATE'], 
		minDepth=cfg['MIN_DEPTH'], initializationMaxTreeDepth=cfg['INITIALIZATION_MAX_TREE_DEPTH'], 
		tournamentSize=cfg['TOURNAMENT_SIZE'], reproductionSize=cfg['REPODUCTION_SIZE'], 
		fitnessType=fitnessType, errorEpsilon=cfg['ERROR_EPSILON'], functions = fs,
		useSSC = cfg['SSC']['USE_SSC'],
		sscLBSS = cfg['SSC']['LBSS'],
		sscUBSS = cfg['SSC']['UBSS'],
		sscMaxTrials = cfg['SSC']['MAX_TRIALS'])

	
	if args.datasetType == "generated":
		X, y = loadGeneratedDataset(args.datapointsFile)
	elif args.datasetType == "yacht":
		X, y = loadYachtDataset(args.datapointsFile)

	print('Xs', X[:5])
	print('ys', y[:5])


	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

	if args.standardizeData:
		from sklearn import preprocessing
		scaler = preprocessing.StandardScaler()
		scaler.fit(X_train)
		X_train = scaler.transform(X_train)
		X_test = scaler.transform(X_test)

	
	dir = './results/GP/'

	if cfg['SSC']['USE_SSC']:
		dir += 'SSC'
	else:
		dir += 'basicGP'

	if not os.path.exists(dir):
		os.makedirs(dir)

	resFile = args.datapointsFile[args.datapointsFile.rfind(os.path.sep) : args.datapointsFile.rfind('.')] + '.txt'
	resFile = dir + resFile
	open(resFile, 'w').close()

	csvFile = resFile[: resFile.rfind('.')] + '.csv'
	open(csvFile, 'w').close()
	if errorType == 'r2_score':
		header = ['Run', 'TrainR2Score', 'TestR2Score', 'BestIndividual', 'BestIndividualSimplified', 'Time', 'SympyEquivalence']
	else:
		header = ['Run', 'TrainError', 'TestError', 'BestIndividual', 'BestIndividualSimplified', 'Time', 'SympyEquivalence']

	with open(csvFile, 'w', encoding='UTF8') as file:
		writer = csv.writer(file)
		writer.writerow(header)

	with open(resFile, 'a+') as file:
		file.write('Population size: ' + str(cfg['POPULATION_SIZE']) + '\n')
		file.write('Max number of generations: ' + str(cfg['MAX_GENERATIONS']) + '\n')
		file.write('Reproduction size: ' + str(cfg['REPODUCTION_SIZE']) + '\n')
		file.write('Mutation rate: ' + str(cfg['MUTATION_RATE']) + '\n')
		file.write('One point mutation rate: ' + str(cfg['OP_MUTATION_RATE']) + '\n')
		file.write('Min tree depth: ' + str(cfg['MIN_DEPTH']) + '\n')
		file.write('Max tree depth in initialization phase: ' + str(cfg['INITIALIZATION_MAX_TREE_DEPTH']) + '\n')
		file.write('Max tree size: ' + str(cfg['MAX_TREE_SIZE']) + '\n')
		file.write('Tournament size: ' + str(cfg['TOURNAMENT_SIZE']) + '\n')
		file.write('Fitness type: ' + str(fitnessType) + '\n')
		file.write('Error type: ' + str(errorType) + '\n')
		file.write('Error epsilon: ' + str(cfg['ERROR_EPSILON']) + '\n')
		if cfg['SSC']['USE_SSC']:
			file.write('LBSS: ' + str(cfg['SSC']['LBSS']) + '\n')
			file.write('UBSS: ' + str(cfg['SSC']['UBSS']) + '\n')
			file.write('Max trials: ' + str(cfg['SSC']['MAX_TRIALS']) + '\n')



	if args.realEquation:
		with open(args.realEquation) as file:
			realEquationSympy = parse_expr(file.readline())


	for run in range(cfg['NUM_RUNS']):

		startTime = time.time()

		gpEstimator.fit(X_train, y_train)

		endTime = time.time() - startTime
		hours, rem = divmod(endTime, 3600)
		minutes, seconds = divmod(rem, 60)
		executionTimeFormated = '{:0>2}:{:0>2}:{:05.2f}'.format(int(hours), int(minutes), seconds)

		bestIndividual = gpEstimator.getBest()
		bestStr = bestIndividual.stringRepresentation()
		print('Best individual:', bestStr)

		bestIndividualSimplified = simplify(bestStr)

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
		elif errorType == 'r2_score':
			trainErr = r2Score(y_train, y_train_pred)
			testErr = r2Score(y_test, y_test_pred)

		if np.isnan(trainErr):
			trainErr = np.inf

		if np.isnan(testErr):
			testErr = np.inf
		
		print('Train' + errorType + ' :', trainErr)
		print('Test' + errorType + ' :', testErr)


		data = [run, trainErr, testErr, bestStr, bestIndividualSimplified, executionTimeFormated]
		if args.realEquation:
			data.append(sympyEquivalence)
		with open(csvFile, 'a+', encoding='UTF8') as file:
			writer = csv.writer(file)
			writer.writerow(data)


	print('Results are written to ' + resFile + '\n and' + csvFile)
	
	


if __name__ == "__main__":
    main()