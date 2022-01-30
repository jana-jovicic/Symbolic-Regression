import numpy as np
from copy import deepcopy
from numpy.random import randint
from numpy.random import random
from GeneticPrograming.ExpressionTreeManipulation.mutation import candidateNodesAtRandomDepth
from GeneticPrograming.ExpressionTreeManipulation.randomTreeGenerator import generateRandomTree

from expression import ConstantNode, SubNode


def SubtreeCrossover( individual, donor ):
	
    # this version of crossover returns 1 child

    nodes1 = individual.GetSubtree()
    nodes2 = donor.GetSubtree()	# no need to deep copy all nodes of parent2

    nodes1 = __GetCandidateNodesAtUniformRandomDepth( nodes1 )
    nodes2 = __GetCandidateNodesAtUniformRandomDepth( nodes2 )

    to_swap1 = nodes1[ randint(len(nodes1)) ]
    to_swap2 = deepcopy( nodes2[ randint(len(nodes2)) ] )	# we deep copy now, only the sutbree from parent2
    to_swap2.parent = None

    p1 = to_swap1.parent

    if not p1:
        return to_swap2

    idx = p1.DetachChild(to_swap1)
    p1.InsertChildAtPosition(idx, to_swap2)

    return individual


def subtreeCrossoverOneCild(parent1, parent2):

    nodes1 = parent1.subtrees()
    nodes2 = parent2.subtrees()

    print("nodes1", nodes1)
    print("nodes2", nodes2)

    nodes1 = candidateNodesAtRandomDepth(nodes1)
    nodes2 = candidateNodesAtRandomDepth(nodes2)

    print("nodes1", nodes1)
    print("nodes2", nodes2)

    toSwap1 = nodes1[randint(len(nodes1))]
    print("toSwap1", toSwap1.stringRepresentation())
    toSwap2 = deepcopy(nodes2[randint(len(nodes2))])
    toSwap2.parent = None
    print("toSwap2", toSwap2.stringRepresentation())

    p1 = toSwap1.parent
    print("p1", p1)

    # root node, toSwap1 does not have parent
    if not p1:
        return toSwap2

    detached = p1.detachChildNode(toSwap1)
    print("detached", detached)
    if detached == "left":
        p1.appendLeft(toSwap2)
    elif detached == "right":
        p1.appendRight(toSwap2)

    return parent1