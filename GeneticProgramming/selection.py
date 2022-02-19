import numpy as np
from copy import deepcopy
from numpy.random import randint

def tournamentSelection(population, reproductionSize, tournamentSize,):
	"""
    A stocastic variation of tournament selection.
    population - initial population from which individuals will be selected
    reproductionSize - number of individuals to be selected
    tournamentSize - number of individuals that compete in tournament
    """

	populationSize = len(population)
	selectedIndividuals = []

	for i in range(reproductionSize):

		best = population[randint(populationSize)]
		for i in range(tournamentSize - 1):
			contestant = population[randint(populationSize)]
			if contestant.fitness < best.fitness:
				best = contestant

		survivor = deepcopy(best)
		selectedIndividuals.append(survivor)

	return selectedIndividuals