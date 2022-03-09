from GeneticProgramming.fitness import FitnessFunction
import numpy as np
import random
from GeneticProgramming.crossover import SSC, subtreeCrossover, subtreeCrossoverOneCild

from expression import *
from GeneticProgramming.randomTreeGenerator import *
from GeneticProgramming.mutation import *

#np.random.seed(1)   # gives semantically similar individuals for X_set1
#np.random.seed(42)  # gives semantically dissimilar individuals for X_set1

def main():

    X_set0 = np.array([[10,20,30]])
    X_set1 = np.array([[10,20,30], [40,50,60]])

    functions = [AddNode(), SubNode(), MulNode(), DivNode()]
    terminals = []
    minHeight = 1
    currMaxDepth = 4
    #constInterval = [0,10]
    varProbability = 0.85

    nFeatures = X_set0.shape[1]
    #nFeatures = X_set1.shape[1]
    for i in range(nFeatures):
        terminals.append(VariableNode(i))

    t = generateRandomTree(functions, terminals, currMaxDepth, currentHeight=0, method='grow' if np.random.random() < 0.5 else 'full', minHeight=minHeight, varProbability=varProbability)
    
    print("Random individual:")
    print(t.stringRepresentation())
    #print(t.height())
    #print(t.depth())
    print(t.value(X_set0))
    print()

    functions = [AddNode(), SubNode(), MulNode(), DivNode(), CosNode(), LogNode(), SinNode()]

    x0 = VariableNode(0)
    x1 = VariableNode(1)
    x2 = VariableNode(2)

    addNode = AddNode()
    addNode.appendLeft(x0)
    addNode.appendRight(x1)
    
    cosNode = CosNode()
    cosNode.appendLeft(x1)

    divNode = DivNode()
    divNode.appendLeft(cosNode)
    divNode.appendRight(addNode)



    subNode = SubNode()
    subNode.appendLeft(x1)
    subNode.appendRight(x0)

    mulNode = MulNode()
    mulNode.appendLeft(subNode)
    mulNode.appendRight(x2)
    
    
    addNodeRoot = AddNode()
    addNodeRoot.appendLeft(divNode)
    addNodeRoot.appendRight(mulNode)

    """
    print("Original individual:")
    print(addNodeRoot.stringRepresentation())
    print(addNodeRoot.value(X_set0))

    mutatedIndividual1 = onePointMutation(addNodeRoot, functions, terminals)
    print("One point mutation:")
    print(mutatedIndividual1.stringRepresentation())
    print(mutatedIndividual1.value(X_set0))

    print("Original individual:")
    print(addNodeRoot.stringRepresentation())
    print(addNodeRoot.value(X_set0))
    print()
    
    mutatedIndividual2 = subtreeMutation(addNodeRoot, functions, terminals, maxHeight=2, minHeight=1)
    print("Subtree mutation:")
    print(mutatedIndividual2.stringRepresentation())
    print(mutatedIndividual2.value(X_set0))

    print("Original individual:")
    print(addNodeRoot.stringRepresentation())
    print(addNodeRoot.value(X_set0))
    print()
    """

    
    x0 = VariableNode(0)
    x1 = VariableNode(1)
    x2 = VariableNode(2)
    logNode = LogNode()
    logNode.appendLeft(x0)
    divNode2 = DivNode()
    sinNode = SinNode()
    sinNode.appendLeft(x1)
    divNode2.appendLeft(sinNode)
    divNode2.appendRight(x2)
    parent2 = MulNode()
    parent2.appendLeft(logNode)
    parent2.appendRight(divNode2)

    """
    print("parent1", addNodeRoot.stringRepresentation())
    print("parent2", parent2.stringRepresentation())
    crossoverChild1 = subtreeCrossoverOneCild(addNodeRoot, parent2)
    print("crossoverChild1", crossoverChild1.stringRepresentation())
    """

    print()
    print("Original individual1:")
    print(addNodeRoot.stringRepresentation())
    print("Original individual2:")
    print(parent2.stringRepresentation())
    print()
    
    child1, child2 = subtreeCrossover(addNodeRoot, parent2)
    print("child1: ", child1.stringRepresentation())
    print("child1: ", child2.stringRepresentation())
    print()
    print("Original individual1:")
    print(addNodeRoot.stringRepresentation())
    print("Original individual2:")
    print(parent2.stringRepresentation())
    print()



    print("--------------------------")
    print("Semantically based crossover")
    print()
    print("Original individual1:")
    print(addNodeRoot.stringRepresentation())
    print("Original individual2:")
    print(parent2.stringRepresentation())
    print()


    # y_real = ((cos(x1) / (x0 + x1)) + (sin(x0) * x2))
    y_set0 = []
    for i in range(len(X_set0)):
        y_set0.append([((np.cos(X_set0[i][1]) / (X_set0[i][0] + X_set0[i][1])) + (np.sin(X_set0[i][0]) * X_set0[i][2]))])
    y_set0 = np.array(y_set0)

    y_set1 = []
    for i in range(len(X_set1)):
        y_set1 = np.array([((np.cos(X_set1[i][1]) / (X_set1[i][0] + X_set1[i][1])) + (np.sin(X_set1[i][0]) * X_set1[i][2]))])
    y_set1 = np.array(y_set1)
    
    fitnessFunction = FitnessFunction(X_set0, y_set0, 'mse')

    child1, child2 = SSC(addNodeRoot, parent2, fitnessFunction.X_train, 1e-4, 0.4, 1)

    print()
    print("child1")
    print(child1.stringRepresentation())
    print("child2")
    print(child2.stringRepresentation())
    print()
    print("Original individual1:")
    print(addNodeRoot.stringRepresentation())
    print("Original individual2:")
    print(parent2.stringRepresentation())
    print()


if __name__ == "__main__":
    main()