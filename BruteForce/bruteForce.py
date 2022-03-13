import inspect
import itertools
import numpy as np
from copy import deepcopy
from numpy.random import randint
from numpy.random import random

from expression import *

class BruteForce():

    def __init__(self,
        X,
        y,
		functions = [AddNode(), SubNode(), MulNode(), DivNode(), LogNode()],
		maxTreeSize = 10,
		errorType = 'mse',
		errorEpsilon = 1e-10,
        maxHours = 1):

        args, _, _, values = inspect.getargvalues(inspect.currentframe())
        values.pop('self')
        for arg, val in values.items():
            setattr(self, arg, val)


    def mse(self, y_real, y_pred):
        return np.mean(np.square(y_real - y_pred))


    def run(self):

        treeHeight = 1

        """
        print(self.X.shape)
        if self.X.shape[1] > 1:
            for equationInstancePoints in self.X:
                xsPermutations = itertools.permutations(equationInstancePoints, 2)
                for pair in xsPermutations:
                    print(pair)
                print('----------')
        """

        terminals = []
        nVariables = self.X.shape[1]
        for i in range(nVariables):
            terminals.append(VariableNode(i))
        print(terminals)

        terminalPermutations = []
        if nVariables > 1:
            for pair in itertools.permutations(terminals, 2):
                terminalPermutations.append(pair)


        # height = 1
        foundSolution = False
        solution = ''

        for func in self.functions:
            print(func)
            for pair in terminalPermutations:
                func.appendLeft(deepcopy(pair[0]))
                func.appendRight(deepcopy(pair[1]))
                print(func.stringRepresentation())
                y_pred = func.value(self.X)
                print(func.value(self.X)[:5])
                err = self.mse(self.y, y_pred)
                print("mse", err)
                if err < self.errorEpsilon:
                    foundSolution = True
                    solution = func
                    break

            if foundSolution:
                break

        print("solution", solution)
        if solution != '':
            print("solution", solution.stringRepresentation())