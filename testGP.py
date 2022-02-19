from GeneticProgramming.GP import GP
from GeneticProgramming.GPEstimator import GeneticProgrammingSymbolicRegressionEstimator
import numpy as np 
import sklearn.datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import scale
from copy import deepcopy

from expression import *


np.random.seed(42)

# Load regression dataset 
X, y = sklearn.datasets.load_boston( return_X_y=True )


# Take a dataset split
X_train, X_test, y_train, y_test = train_test_split( X, y, test_size=0.5, random_state=42 )


X_train = X_train[:5]
y_train = y_train[:5]
X_test = X_test[:5]
y_test = y_test[:5]

print(X_train)
print(y_train)

# Initalize GP estimator
use_linear_scaling=False
gpEstimator = GeneticProgrammingSymbolicRegressionEstimator(populationSize=50, maxGenerations=25, verbose=True, maxTreeSize=100, crossoverRate=0.0, mutationRate=0.33, opMutationRate=0.33, 
    minHeight=2, initializationMaxTreeHeight=4, 
	tournamentSize=4,
	functions = [AddNode(), SubNode(), MulNode(), DivNode()])

gpEstimator.fit(X_train, y_train)

# Get final result
bestIndividual = gpEstimator.getBest()
bestStr = bestIndividual.stringRepresentation()
print('Best individual found:', bestStr)

# Show mean squared error
print('Train MSE:',np.mean(np.square(y_train - gpEstimator.predict(X_train))))
print('Test MSE:',np.mean(np.square(y_test - gpEstimator.predict(X_test))))