import random
from GeneticProgramming.randomTreeGenerator import generateRandomTree
from GeneticProgramming.fitness import FitnessFunction
import numpy as np

from expression import *



def main():

    X_set0 = np.array([[10,20,30]])
    X_set1 = np.array([[10,20,30], [40,50,60]])

    # y = (( x0 / x0 ) + ( x2 - x1 ))
    y_set0 = np.array([11.0])
    y_set1 = np.array([11.0, 11.0])

    x0 = VariableNode(0)
    x1 = VariableNode(1)
    x2 = VariableNode(2)

    # Individual for evaluation: (( x2 / x0 ) + ( x2 - x1 ))

    divNode1 = DivNode()
    divNode1.appendLeft(x2)
    divNode1.appendRight(x0)

    subNode1 = SubNode()
    subNode1.appendLeft(x2)
    subNode1.appendRight(x1)

    addNode1 = AddNode()
    addNode1.appendLeft(divNode1)
    addNode1.appendRight(subNode1)
    
    print("Individual for evaluation:")
    print(addNode1.stringRepresentation())
    print(addNode1.value(X_set0))


    fitness_function = FitnessFunction(X_set1, y_set1)
    fitness_function.evaluate(addNode1)
    

if __name__ == "__main__":
    main()