import csv
import time
import os, argparse
from VNP.basicVNP import VNP
from VNP.localSearch import r2Score
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import scale
from copy import deepcopy

from sympy import simplify
from sympy.parsing.sympy_parser import parse_expr

from expression import *
from util.loadDatasets import loadGeneratedDataset, loadYachtDataset
from util.yamlParser import getConfig

np.random.seed(42)

functionNames = {"add": AddNode(), "sub": SubNode(), "mul": MulNode(), "div": DivNode(), "pow": PowNode(), "log": LogNode(), "exp": ExpNode(), "sin": SinNode(), "cos": CosNode()}


def main():


    parser = argparse.ArgumentParser(description='VNP')
    parser.add_argument("--datasetType", type=str, default='generated', help='type of dataset (could be: "generated", "real")')
    parser.add_argument("--standardizeData", default=False, action='store_true', help='flag to indicate whether or not to standardize data')
    parser.add_argument("--config", type=str, default='./configs/vnp.yaml', help='path to configuration file')
    parser.add_argument('--datapointsFile', required=False, default='generatedDatasets/f1.txt', type=str, help='path to file that contains datapoints')
    parser.add_argument('--realEquation', required=False, default='generatedDatasets/f1_solution.txt', type=str, help='path to file that contains exact solution')
    args = parser.parse_args()

    if args.datasetType == "generated" and args.datapointsFile is None:
        parser.error('\t\t File fith datapoints must be provided. Example usage is in file startGP.sh')

    cfg = getConfig(args.config)
    print(cfg)


    if args.datasetType == "generated":
        X, y = loadGeneratedDataset(args.datapointsFile)
    elif args.datasetType == "yacht":
        X, y = loadYachtDataset(args.datapointsFile)

    #print('Xs', X[:5])
    #print('ys', y[:5])


    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    if args.standardizeData:
        from sklearn import preprocessing
        scaler = preprocessing.StandardScaler()
        scaler.fit(X_train)
        X_train = scaler.transform(X_train)
        X_test = scaler.transform(X_test)


    fs = [functionNames[f] for f in cfg['FUNCTIONS']]

    terminals = []
    nFeatures = X_train.shape[1]
    for i in range(nFeatures):
        terminals.append(VariableNode(i))

   
    dir = './results/VNP'

    if not os.path.exists(dir):
        os.makedirs(dir)
        
    resFile = args.datapointsFile[args.datapointsFile.rfind(os.path.sep) : args.datapointsFile.rfind('.')] + '.txt'
    resFile = dir + resFile
    open(resFile, 'w').close()

    csvFile = resFile[: resFile.rfind('.')] + '.csv'
    open(csvFile, 'w').close()
    header = ['Run', 'TrainR2Score', 'TestR2Score', 'BestSolution', 'BestSolutionSimplified', 'IterationOfBestSolution', 'Time', 'SympyEquivalence']

    with open(csvFile, 'w', encoding='UTF8') as file:
        writer = csv.writer(file)
        writer.writerow(header)

    with open(resFile, 'a+') as file:
        file.write('K_MAX: ' + str(cfg['K_MAX']) + '\n')
        file.write('Min depth of initial tree: ' + str(cfg['MIN_INIT_TREE_DEPTH']) + '\n')
        file.write('Max depth of initial tree: ' + str(cfg['MAX_INIT_TREE_DEPTH']) + '\n')
        file.write('Max depth of created trees: ' + str(cfg['MAX_TREE_DEPTH']) + '\n')
        file.write('Max number of iterations: ' + str(cfg['MAX_ITERATIONS']) + '\n')
        file.write('Max number of hours for program execution: ' + str(cfg['MAX_HOURS']) + '\n')
        

    if args.realEquation:
        with open(args.realEquation) as file:
            realEquationSympy = parse_expr(file.readline())


    for run in range(cfg['NUM_RUNS']):

        startTime = time.time()

        vnp = VNP(terminals=terminals, functions=fs, minInitTreeDepth = cfg['MIN_INIT_TREE_DEPTH'], maxInitTreeDepth = cfg['MAX_INIT_TREE_DEPTH'], 
            kMax = cfg['K_MAX'], maxIterations=cfg['MAX_ITERATIONS'], maxHours=cfg['MAX_HOURS'],
            maxTreeDepth = cfg['MAX_TREE_DEPTH'])

        vnp.fit(X_train, y_train)

        endTime = time.time() - startTime
        hours, rem = divmod(endTime, 3600)
        minutes, seconds = divmod(rem, 60)
        executionTimeFormated = '{:0>2}:{:0>2}:{:05.2f}'.format(int(hours), int(minutes), seconds)

        bestSolution = vnp.getBest()
        bestStr = bestSolution.stringRepresentation()
        print('Best solution:', bestStr)

        bestSolutionScore = vnp.getBestScore()
        print('Best solution score:', bestSolutionScore)

        bestSolutionSimplified = simplify(bestStr)

        bestSolutionSympy = parse_expr(bestStr)
        equationsDiff = bestSolutionSympy - realEquationSympy
        diffSimplified = simplify(equationsDiff)
        sympyEquivalence = str(diffSimplified == 0)

        y_train_pred = vnp.predict(X_train)
        y_test_pred = vnp.predict(X_test)

        trainScore = r2Score(y_train, y_train_pred)
        testScore = r2Score(y_test, y_test_pred)

        if np.isnan(trainScore):
            trainScore = -np.inf

        if np.isnan(testScore):
            testScore = -np.inf
        
        print('Train r2 score:', trainScore)
        print('Test r2 score:', testScore)

        data = [run, trainScore, testScore, bestStr, bestSolutionSimplified, vnp.bestSolutionIteration, executionTimeFormated]
        if args.realEquation:
            data.append(sympyEquivalence)
        with open(csvFile, 'a+', encoding='UTF8') as file:
            writer = csv.writer(file)
            writer.writerow(data)

    
    print('Results are written to ' + resFile + '\n and' + csvFile)

if __name__ == "__main__":
    main()