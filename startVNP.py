import csv
import time
import os, argparse
from VNP.basicVNP import VNP
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import scale
from copy import deepcopy

from sympy import simplify
from sympy.parsing.sympy_parser import parse_expr

from expression import *
from util.loadDatasets import loadGeneratedDataset, loadRealDataset, loadSynchronousMachineDataset, loadYachtDataset
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
    elif args.datasetType == "real":
        fileType = args.datapointsFile[args.datapointsFile.rfind('.')+1:]
        #print(fileType)
        X, y = loadRealDataset(args.datapointsFile, fileType)
    elif args.datasetType == "synchronous_machine":
        X, y = loadSynchronousMachineDataset(args.datapointsFile)
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


    fs = [functionNames[f] for f in cfg['FUNCTIONS']]

    terminals = []
    nFeatures = X_train.shape[1]
    for i in range(nFeatures):
        terminals.append(VariableNode(i))

    print("terminals", terminals)
    print("functions", fs)
    
    vnp = VNP(X = X_train, y = y_train, terminals=terminals, functions=fs, minDepth = cfg['MIN_INIT_TREE_DEPTH'],
                maxDepth = cfg['MAX_INIT_TREE_DEPTH'], kMax = cfg['K_MAX'], maxIterations=cfg['MAX_ITERATIONS'], maxHours=cfg['MAX_HOURS'])

    vnp.run()


if __name__ == "__main__":
    main()