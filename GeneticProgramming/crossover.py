import numpy as np
from copy import deepcopy
from numpy.random import randint
from numpy.random import random
from GeneticProgramming.mutation import candidateNodesAtRandomDepth
from GeneticProgramming.randomTreeGenerator import generateRandomTree

from expression import SubNode


def subtreeCrossoverOneCild(individual1, individual2):

    parent1 = deepcopy(individual1)
    parent2 = deepcopy(individual2)

    nodes1 = parent1.subtrees()
    nodes2 = parent2.subtrees()

    nodes1 = candidateNodesAtRandomDepth(nodes1)
    nodes2 = candidateNodesAtRandomDepth(nodes2)

    toSwap1 = nodes1[randint(len(nodes1))]
    toSwap2 = deepcopy(nodes2[randint(len(nodes2))])
    toSwap2.parent = None

    p1 = toSwap1.parent

    # root node, toSwap1 does not have parent
    if not p1:
        return toSwap2

    detached = p1.detachChildNode(toSwap1)
    if detached == "left":
        p1.appendLeft(toSwap2)
    elif detached == "right":
        p1.appendRight(toSwap2)

    return parent1



def subtreeCrossover(individual1, individual2):

    parent1 = deepcopy(individual1)
    parent2 = deepcopy(individual2)

    nodes1 = parent1.subtrees()
    nodes2 = parent2.subtrees()

    #print("nodes1", nodes1)
    #print("nodes2", nodes2)

    nodes1 = candidateNodesAtRandomDepth(nodes1)
    nodes2 = candidateNodesAtRandomDepth(nodes2)

    toSwap1 = nodes1[randint(len(nodes1))]
    #print("toSwap1", toSwap1.stringRepresentation())
    toSwap2 = nodes2[randint(len(nodes2))]
    #print("toSwap2", toSwap2.stringRepresentation())

    p1 = toSwap1.parent
    #print("p1", p1.stringRepresentation())

    p2 = toSwap2.parent
    #print("p2", p2.stringRepresentation())

    if not p1:
        parent1 = toSwap2

    if not p2:
        parent2 = toSwap1

    if p1:
        if p1.left == toSwap1:
            p1.left = toSwap2
            toSwap2.parent = p1
            if p2:
                if p2.left == toSwap2:
                    p2.left = toSwap1
                    toSwap1.parent = p2
                else:
                    p2.right = toSwap1
                    toSwap1.parent = p2

        else:
            p1.right = toSwap2
            toSwap2.parent = p1
            if p2:
                if p2.left == toSwap2:
                    p2.left = toSwap1
                    toSwap1.parent = p2
                else:
                    p2.right = toSwap1
                    toSwap1.parent = p2


    return parent1, parent2


# ------------------------------------------


def SSC(individual1, individual2, X, LBSS, UBSS, maxTrials):

    crossoverExecuted = False

    for i in range(maxTrials):

        child1 = deepcopy(individual1)
        child2 = deepcopy(individual2)

        nodes1 = child1.subtrees()
        nodes2 = child2.subtrees()

        #print("nodes1", nodes1)
        #print("nodes2", nodes2)

        nodes1 = candidateNodesAtRandomDepth(nodes1)
        nodes2 = candidateNodesAtRandomDepth(nodes2)

        subtree1 = nodes1[randint(len(nodes1))]
        print("subtree1", subtree1.stringRepresentation())
        subtree2 = nodes2[randint(len(nodes2))]
        print("subtree2", subtree2.stringRepresentation())


        # Sampling Semantics of subtree1
        ps = subtree1.value(X)
        print("SS subtree1", ps)

        # Sampling Semantics of subtree2
        qs = subtree2.value(X)
        print("SS subtree2", qs)

        # Sampling Semantics Distance
        # SSD(St1, St2) = (|p1 − q1| + |p2 − q2| + .... + |pN − qN|) / N
        SSD = 0
        nPoints = len(X)
        for i in range(nPoints):
            SSD += np.abs(ps[i] - qs[i])
        SSD /= nPoints
        print("SSD", SSD)


        # Semantic Similarity
        SS = LBSS < SSD < UBSS
        print("Semantic Similarity: ", SS)


        if SS:

            # execute crossover
            p1 = subtree1.parent
            #print("p1", p1.stringRepresentation())

            p2 = subtree2.parent
            #print("p2", p2.stringRepresentation())

            if not p1:
                child1 = subtree2

            if not p2:
                child2 = subtree1

            if p1:
                if p1.left == subtree1:
                    p1.left = subtree2
                    subtree2.parent = p1
                    if p2:
                        if p2.left == subtree2:
                            p2.left = subtree1
                            subtree1.parent = p2
                        else:
                            p2.right = subtree1
                            subtree1.parent = p2

                else:
                    p1.right = subtree2
                    subtree2.parent = p1
                    if p2:
                        if p2.left == subtree2:
                            p2.left = subtree1
                            subtree1.parent = p2
                        else:
                            p2.right = subtree1
                            subtree1.parent = p2


            crossoverExecuted = True
            break


    if not crossoverExecuted:
        child1, child2 = subtreeCrossover(individual1, individual2)


    return child1, child2