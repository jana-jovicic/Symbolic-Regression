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


def loadDEEDataset(datapointsFile):
    X, y = [], []

    with open(datapointsFile, 'r') as file:
        lines = file.readlines()
        
        for line in lines:

            if line[0] == '@':
                continue

            line = line.replace(', ', ' ')
            line = line.strip().split(' ')
            line = list(filter(lambda a: a != '', line))

            xs = [float(x) for x in line[:-1]]
            X.append(xs)
            y.append(float(line[-1]))
    return np.array(X), np.array(y)



def loadAirfoilDataset(datapointsFile):

    X, y = [], []
	
    with open(datapointsFile, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.split('\t')
            xs = [float(x) for x in line[:-1]]
            X.append(xs)
            y.append(float(line[-1]))
    return np.array(X), np.array(y)
