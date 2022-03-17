import csv
import time
import os, argparse
import numpy as np
from numpy.random import randint
from numpy.random import random

from expression import *
from BruteForce.bruteForce import BruteForce
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

    parser = argparse.ArgumentParser(description='GP')
    parser.add_argument("--config", type=str, default='./configs/gp.yaml', help='path to configuration file')
    parser.add_argument('--datapointsFile', default='generatedDatasets/f1.txt', type=str, help='path to file that contains datapoints')
    args = parser.parse_args()

    cfg = getConfig(args.config)
    print(cfg)

    fs = [functionNames[f] for f in cfg['FUNCTIONS']]
    print(fs)

    errorType = cfg['ERROR_TYPE']

    X, y = loadDataset(args.datapointsFile)
    print('Xs', X[:5])
    print('ys', y[:5])


    bp = BruteForce(X, y, 
        functions = fs,
		maxTreeSize = 10,
		errorType = cfg['ERROR_TYPE'],
		errorEpsilon = cfg['ERROR_EPSILON'],
        maxHours = cfg['MAX_HOURS'])
    
    foundExactSolution, exactSolution, exactSolutionError, nearestBestSolution, nearestBestSolutionError = bp.run()

    print("foundExactSolution", foundExactSolution)
    if foundExactSolution:
        print("exactSolution", exactSolution.stringRepresentation())
        print("exactSolutionError", exactSolutionError)

    print("nearestBestSolution", nearestBestSolution.stringRepresentation())
    print("nearestBestSolutionError", nearestBestSolutionError)


if __name__ == "__main__":
    main()
