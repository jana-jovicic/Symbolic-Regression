from expression import EphemeralRandomConstantNode
import numpy as np
from copy import deepcopy
from numpy.random import randint
from numpy.random import random
from GeneticProgramming.randomTreeGenerator import generateRandomTree


def onePointMutation(individual, functions, terminalVars):

    newIndividual = deepcopy(individual)

    subtreeNodes = newIndividual.subtrees()
    #print(subtreeNodes)
    mutationProb = 1.0/len(subtreeNodes)
    #print(mutationProb)
    varProb = 0.95
    
    arityFunctionsMap = {}
    for f in functions:
        arity = f.arity
        if arity not in arityFunctionsMap:
            arityFunctionsMap[arity] = [f]
        else:
            arityFunctionsMap[arity].append(f)

    #print("arityFunctionsMap", arityFunctionsMap)

    for i in range(len(subtreeNodes)):
        r = random()
        
        """
        #for testing
        if i == 1:
            mutationProb = 1
        else:
            mutationProb = 0
        """
        

        if r < mutationProb:
            arity = subtreeNodes[i].arity 

            if arity == 0:
                # For new node choose variable with greater probability than constant
                if random() < varProb:
                    randIdx = randint(len(terminalVars))
                    newNode = deepcopy(terminalVars[randIdx])
                else:
                    newNode = EphemeralRandomConstantNode()
                    #randConst = randint(constInterval[0],constInterval[1])
                    #newNode = ConstantNode(randConst)
            else:
                randIdx = randint(len(arityFunctionsMap[arity]))
                #print("randIdx", randIdx)
                newNode = deepcopy(arityFunctionsMap[arity][randIdx])
            #print("newNode", newNode)

            # update link to left and right subtree
            if arity > 0:
                newNode.appendLeft(subtreeNodes[i].left)
                if arity == 2:
                    newNode.appendRight(subtreeNodes[i].right)

            #print("newNode left child:", newNode.left)
            #print("newNode right child:", newNode.right)

            # update link to parent node
            parent = subtreeNodes[i].parent
        
            if parent:
                #print("parent", parent)
                #print("subtreeNodes[i]", subtreeNodes[i])
                #print("-------")
                detached = parent.detachChildNode(subtreeNodes[i])
                #print("detached", detached)
                if detached == "left":
                    parent.appendLeft(newNode)
                elif detached == "right":
                    parent.appendRight(newNode)

                #print("parent left child:", parent.left)
                #print("parent right child:", parent.right)
            else:
                subtreeNodes[i] = newNode
                newIndividual = newNode
                #print("individual",individual)

    return newIndividual




def subtreeMutation(individual, functions, terminals, X, maxHeight=4, minDepth=2):

    newIndividual = deepcopy(individual)

    newBranch = generateRandomTree(functions, terminals, maxHeight, minDepth)
    #print("newBranch", newBranch.stringRepresentation())
    
    while not newBranch.isFeasible(X):
        newBranch = generateRandomTree(functions, terminals, maxHeight, minDepth)
    

    subtreeNodes = newIndividual.subtrees()
    #print("subtreeNodes", subtreeNodes)

    subtreeNodes = candidateNodesAtRandomDepth(subtreeNodes)
    #print("subtreeNodes", subtreeNodes)

    toReplace = subtreeNodes[randint(len(subtreeNodes))]
    #print("toReplace", toReplace.stringRepresentation())

    # ograniciti da ne moze da se menja za depth=0 ?
    if toReplace.parent == None:
        #del individual
        return newIndividual

    parent = toReplace.parent
    detached = parent.detachChildNode(toReplace)
    if detached == "left":
        parent.appendLeft(newBranch)
    elif detached == "right":
        parent.appendRight(newBranch)

    return newIndividual


def candidateNodesAtRandomDepth(nodes):

    depths = np.unique([x.depth() for x in nodes])
    #print("depths", depths)
    chosenDepth = depths[randint(len(depths))]
    #print("chosenDepth", chosenDepth)
    candidates = [x for x in nodes if x.depth() == chosenDepth]
    return candidates