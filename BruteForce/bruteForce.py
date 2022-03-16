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
        nextHeightTerminals = []
        nVariables = self.X.shape[1]
        for i in range(nVariables):
            terminals.append(VariableNode(i))
            nextHeightTerminals.append(VariableNode(i))
        print("terminals", terminals)
        print(type(terminals))

        """
        terminalPermutations = []
        if nVariables > 1:
            for pair in itertools.product(terminals, repeat=2):
                terminalPermutations.append(pair)
                print(pair)
        """



        height = 0

        while True:

            
            print("height", height)

            terminalPermutations = []
            for pair in itertools.product(terminals, repeat=2):
                terminalPermutations.append(pair)
                #print("pair:", pair[0].stringRepresentation(), ", ", pair[1].stringRepresentation())

            foundSolution, solution, functions = self.buildTree(terminalPermutations)
            print('foundSolution', foundSolution)
            print('solution', solution)
            #print('functions', functions)

            # -----------
            # just for debug
            height += 1
            if height == 3:
                break
            # ----------

            
            for function in functions:
                if any(terminal.stringRepresentation() == function.stringRepresentation() for terminal in terminals):
                    continue
                else:
                    terminals.append(deepcopy(function))
                    """
                    print(function.stringRepresentation())
                    print(terminals[2].stringRepresentation())
                    print(function == terminals[2])
                    print(function.stringRepresentation() == terminals[2].stringRepresentation())
                    print('//////////')
                    """
                    

            for term in terminals:
                print("term", term.stringRepresentation())

            """
            terminalPermutations = []
            for pair in itertools.product(terminals, repeat=2):
                    terminalPermutations.append(pair)
            """

            #for pair in terminalPermutations:
            #    print("pair", pair[0].stringRepresentation(),  pair[1].stringRepresentation())


            print('------------------')
        
        

        """
        # height = 1
        foundSolution = False
        solution = ''

        for func in self.functions:
            print(func)
            n = len(terminalPermutations)
            #for pair in terminalPermutations:
            for i in range(n):
                pair = terminalPermutations[i]
                func.appendLeft(deepcopy(pair[0]))

                if func.arity == 1:
                    #print(pair)
                    #print(terminalPermutations[i-1])
                    if pair[0] == terminalPermutations[i-1][0]:
                        print("same")
                        continue

                if func.arity > 1:
                    func.appendRight(deepcopy(pair[1]))
                print(func.stringRepresentation())
                y_pred = func.value(self.X)
                y_pred = [np.inf if np.isnan(y) else y for y in y_pred]
                print(y_pred[:5])
                err = self.mse(self.y, y_pred)
                print("mse", err)
                if err < self.errorEpsilon:
                    foundSolution = True
                    solution = func
                    break

            if foundSolution:
                break

        print("solution:", solution)
        if solution != '':
            print("solution:", solution.stringRepresentation())
        """


    
    def buildTree(self, terminalPermutations):

        functions = []
        foundSolution = False
        solution = ''

        for func in self.functions:
            #print(func)
            n = len(terminalPermutations)
            #for pair in terminalPermutations:
            for i in range(n):
                pair = terminalPermutations[i]
                func.appendLeft(deepcopy(pair[0]))

                if func.arity == 1:
                    #print(pair)
                    #print(terminalPermutations[i-1])
                    if pair[0] == terminalPermutations[i-1][0]:
                        #print("same")
                        continue

                if func.arity > 1:
                    func.appendRight(deepcopy(pair[1]))
                #print(func.stringRepresentation())

                functions.append(deepcopy(func))

                y_pred = func.value(self.X)
                y_pred = [np.inf if np.isnan(y) else y for y in y_pred]
                #print(y_pred[:5])
                err = self.mse(self.y, y_pred)
                #print("mse", err)
                if err < self.errorEpsilon:
                    foundSolution = True
                    solution = func
                    break

            if foundSolution:
                break

        return foundSolution, solution, functions
            