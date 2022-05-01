import numpy as np
import pandas as pd

def loadGeneratedDataset(datapointsFile):
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


def loadXLS(datapointsFile):
    X, y = [], []
    df = pd.read_excel(datapointsFile)

    for index, row in df.iterrows():
        n = len(row)
        xs = [float(row[i]) for i in range(n-1)]
        X.append(xs)
        y.append(float(row[-1]))
   
    return np.array(X), np.array(y)

def loadCSV(datapointsFile):
    X, y = [], []
    df = pd.read_csv(datapointsFile)

    for index, row in df.iterrows():
        line = row[0].split(';')
        xs = [float(x) for x in line[:-1]]
        X.append(xs)
        y.append(float(line[-1]))
   
    return np.array(X), np.array(y)

def loadRealDataset(datapointsFile, fileType):
    if fileType == 'xls' or fileType == 'xlsx':
        X, y = loadXLS(datapointsFile)
    elif fileType == 'csv':
        X, y = loadCSV(datapointsFile)
    return X, y


def loadSynchronousMachineDataset(datapointsFile):
    X, y = [], []
    df = pd.read_csv(datapointsFile)

    #print(df.head())

    for index, row in df.iterrows():
        n = len(row)
        xs = []
        for i in range(n-1):
            xs.append(float(row[i]))
        X.append(xs)
        y.append(float(row[-1]))
   
    return np.array(X), np.array(y)


def loadYachtDataset(datapointsFile):
    X, y = [], []

    with open(datapointsFile, 'r') as file:
        lines = file.readlines()[:-1]
        for line in lines:
            line = line.strip().split(' ')
            #print(line)
            line = list(filter(lambda a: a != '', line))
            xs = [float(x) for x in line[:-1]]
            X.append(xs)
            y.append(float(line[-1]))
    return np.array(X), np.array(y)