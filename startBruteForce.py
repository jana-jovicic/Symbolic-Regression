import csv
import time
import os, argparse
import numpy as np

from sympy import simplify
from sympy.parsing.sympy_parser import parse_expr

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
    parser.add_argument('--realEquation', default='generatedDatasets/f1_solution.txt', type=str, help='path to file that contains exact solution')
    args = parser.parse_args()

    cfg = getConfig(args.config)
    print(cfg)

    fs = [functionNames[f] for f in cfg['FUNCTIONS']]
    print(fs)

    errorType = cfg['ERROR_TYPE']

    X, y = loadDataset(args.datapointsFile)
   
    dir = './results/BruteForce/'
    if not os.path.exists(dir):
        os.makedirs(dir)

    resFile = args.datapointsFile[args.datapointsFile.rfind(os.path.sep) : ]
    resFile = dir + resFile
    
    csvFile = resFile[: resFile.rfind('.')] + '.csv'
    open(csvFile, 'w').close()
    header = ['realEquation', 'foundExactSolution', 'exactSolution', 'sympyEquivalence', 'nearestBestSolution', 'nearestBestSolutionError', 'Time (h:m:s)', 'maxGivenHours']
    data = []

    if args.realEquation:
        with open(args.realEquation) as file:
            realEquationSympy = parse_expr(file.readline())
            data.append(realEquationSympy)
    else:
        data.append('/')

    with open(csvFile, 'w', encoding='UTF8') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        if args.realEquation:
            writer.writerow([realEquationSympy, '/', '/', '/', '/', '/', '/', '/'])
        else:
            writer.writerow(['/', '/', '/', '/', '/', '/', '/', '/'])

    startTime = round(time.time())

    bp = BruteForce(X, y, 
        functions = fs,
		errorType = cfg['ERROR_TYPE'],
		errorEpsilon = cfg['ERROR_EPSILON'],
        maxHours = cfg['MAX_HOURS'],
        csvFile = csvFile)

    foundExactSolution, exactSolution, exactSolutionError, nearestBestSolution, nearestBestSolutionError = bp.run()

    executionTime = round(time.time()) - startTime

    hours, rem = divmod(executionTime, 3600)
    minutes, seconds = divmod(rem, 60)
    executionTimeFormated = '{:0>2}:{:0>2}:{:05.2f}'.format(int(hours), int(minutes), seconds)


    print("Found Exact Solution: ", foundExactSolution)
    if foundExactSolution:
        print("Exact Solution:", exactSolution.stringRepresentation())
        #print("exactSolutionError", exactSolutionError)

        data.append(str(foundExactSolution))
        data.append(exactSolution.stringRepresentation())

        # check with sympy if it is exactly equivalent
        if args.realEquation:
            exactSolutionSympy = parse_expr(exactSolution.stringRepresentation())
            #print("realEquationSympy",realEquationSympy)
            equationsDiff = exactSolutionSympy - realEquationSympy
            #print("equationsDiff", equationsDiff)   
            diffSimplified = simplify(equationsDiff)
            #print("diffSimplified simplified", diffSimplified)  
            data.append(str(diffSimplified == 0))
        else:
            data.append('/')

        
    else:
        data.append('False')
        data.append('/')
        data.append('/')
    data.append(nearestBestSolution.stringRepresentation())
    data.append(str(nearestBestSolutionError))

    data.append(str(executionTimeFormated))
    data.append(str(cfg['MAX_HOURS']))


    with open(csvFile, 'w', encoding='UTF8') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerow(data)


if __name__ == "__main__":
    main()
