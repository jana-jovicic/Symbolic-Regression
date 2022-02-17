import numpy as np
from copy import deepcopy
from numpy.random import randint
from numpy.random import random

from expression import ConstantNode


def generateRandomTree(functions, terminalVars, maxHeight, currentHeight=0, method='grow', minHeight=2, constInterval=[0,10], varProbability=0.8):

    #print("method", method)
    #print("functions", functions)
    #print("terminals", terminalVars)
    #print("currentHeight", currentHeight)
    #print("maxHeight", maxHeight)

    if currentHeight == maxHeight:
        # Only terminal can be appended in order not to exceed maxHeight

        if random() < varProbability:
            randIdx = randint(len(terminalVars))
            t = deepcopy(terminalVars[randIdx])
            #print("terminal t:", t)
        else:
            randConst = randint(constInterval[0],constInterval[1])
            t = ConstantNode(randConst)
    else:
        if method == 'grow' and currentHeight >= minHeight:
            termsAndFuncs = terminalVars + functions
            randIdx = randint(len(termsAndFuncs))
            t = deepcopy(termsAndFuncs[randIdx])
        elif method == 'full' or (method == 'grow' and currentHeight < minHeight):
            # Only function append is allowed
            # If terminal is appended, tree would be lower than minHeight
            randIdx = randint(len(functions))
            t = deepcopy(functions[randIdx])
        else:
            raise ValueError('Not supported tree generation method')

        #print("t:", t)


        if t.arity > 0:
            leftChild = generateRandomTree(functions, terminalVars, maxHeight, currentHeight=currentHeight+1, method=method, minHeight=minHeight, constInterval=constInterval, varProbability=varProbability)
            #print("arity leftChild", leftChild)
            t.appendLeft(leftChild)
        if t.arity == 2:
            rightChild = generateRandomTree(functions, terminalVars, maxHeight, currentHeight = currentHeight+1, method=method, minHeight=minHeight, constInterval=constInterval, varProbability=varProbability)
            #print("arity rightChild", rightChild)
            t.appendRight(rightChild)

        #print("t string:", t.stringRepresentation())

    return t

