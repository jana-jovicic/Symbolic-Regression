import numpy as np
from copy import deepcopy
from numpy.random import randint
from numpy.random import random

from expression import EphemeralRandomConstantNode


def generateRandomTree(functions, terminalVars, maxHeight, currentHeight=0, method='grow', minDepth=2, varProbability=0.8):


    if currentHeight == maxHeight:
        # Only terminal can be appended in order not to exceed maxHeight

        if random() < varProbability:
            randIdx = randint(len(terminalVars))
            t = deepcopy(terminalVars[randIdx])
            #print("terminal t:", t)
        else:
            t = EphemeralRandomConstantNode()
    else:
        if method == 'grow' and currentHeight >= minDepth:
            termsAndFuncs = terminalVars + functions
            randIdx = randint(len(termsAndFuncs))
            t = deepcopy(termsAndFuncs[randIdx])
        elif method == 'full' or (method == 'grow' and currentHeight < minDepth):
            # Only function append is allowed
            # If terminal is appended, tree would be lower than minDepth
            randIdx = randint(len(functions))
            t = deepcopy(functions[randIdx])
        else:
            raise ValueError('Not supported tree generation method')


        if t.arity > 0:
            leftChild = generateRandomTree(functions, terminalVars, maxHeight, currentHeight=currentHeight+1, method=method, minDepth=minDepth, varProbability=varProbability)
            #print("arity leftChild", leftChild)
            t.appendLeft(leftChild)

        if t.arity == 2:
            rightChild = generateRandomTree(functions, terminalVars, maxHeight, currentHeight = currentHeight+1, method=method, minDepth=minDepth, varProbability=varProbability)
            t.appendRight(rightChild)


    return t

