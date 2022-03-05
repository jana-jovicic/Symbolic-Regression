import inspect
from GeneticProgramming.ExpressionTreeManipulation.crossover import subtreeCrossover
from GeneticProgramming.ExpressionTreeManipulation.mutation import subtreeMutation, onePointMutation
from GeneticProgramming.ExpressionTreeManipulation.randomTreeGenerator import generateRandomTree
from GeneticProgramming.selection import tournamentSelection
import numpy as np
from numpy.random import random, randint
import time
from copy import deepcopy

class GP:

    def __init__(
        self,
        fitnessFunction,
        functions,
        terminals,
        populationSize = 500,
        mutationRate = 0.5,
        opMutationRate = 0.0,
        maxEvaluations = -1,
        maxGenerations = -1,
        maxTime = -1,
        minHeight = 2,
        initializationMaxTreeHeight = 4,
        maxTreeSize = 10,
        tournamentSize = 4,
        reproductionSize = 200,
        verbose = False):

        args, _, _, values = inspect.getargvalues(inspect.currentframe())
        values.pop('self')
        for arg, val in values.items():
            setattr(self, arg, val)

        self.population = []
        self.generations = 0


    def stopCondition(self):
        terminate = False
        elapsedTime = time.time() - self.startTime
        if self.maxEvaluations > 0 and self.fitnessFunction.evaluations >= self.maxEvaluations:
            terminate = True
        elif self.maxGenerations > 0 and self.generations >= self.maxGenerations:
            terminate = True
        elif self.maxTime > 0 and elapsedTime >= self.maxTime:
            terminate = True

        if terminate and self.verbose:
            print('Terminating at\n\t', self.generations, 'generations\n\t', self.fitnessFunction.evaluations, 'evaluations\n\t', np.round(elapsedTime,2), 'seconds')

        return terminate


    def initialPopulation(self):

        population = []
        curretMaxDepth = self.minHeight
        initDepthInterval = self.populationSize / (self.initializationMaxTreeHeight - self.minHeight + 1)
        nextDepthInterval = initDepthInterval

        for i in range(self.populationSize):
            if i >= nextDepthInterval:
                nextDepthInterval += initDepthInterval
                curretMaxDepth += 1

            t = generateRandomTree( self.functions, self.terminals, curretMaxDepth, currentHeight=0, 
                method='grow' if np.random.random() < 0.5 else 'full', minHeight=self.minHeight)
            self.fitnessFunction.evaluate(t)
            population.append(t)
        
        return population


    def createGeneration(self, individualsForReproduction):

        offsprings = []
        while len(offsprings) < self.populationSize:

            parents = np.random.choice(individualsForReproduction, 2)
            child1, child2 = subtreeCrossover(parents[0], parents[1])

            if random() < self.mutationRate:
                child1 = subtreeMutation(child1, self.functions, self.terminals, maxHeight=self.initializationMaxTreeHeight, minHeight=self.minHeight)
            if random() < self.mutationRate:
                child2 = subtreeMutation(child2, self.functions, self.terminals, maxHeight=self.initializationMaxTreeHeight, minHeight=self.minHeight)

            if random() < self.opMutationRate:
                child1 = onePointMutation(child1, self.functions, self.terminals)
            if random() < self.opMutationRate:
                child2 = onePointMutation(child2, self.functions, self.terminals)

            
            # check if children meet constraints	
            invalidChild1 = False
            if (self.maxTreeSize > -1 and len(child1.subtrees()) > self.maxTreeSize):
                #print("Child1 len in maxTreeSize", len(child1.subtrees()))
                invalidChild1 = True
            elif (child1.height() < self.minHeight):
                invalidChild1 = True

            invalidChild2 = False
            if (self.maxTreeSize > -1 and len(child2.subtrees()) > self.maxTreeSize):
                #print("Child2 len in maxTreeSize", len(child2.subtrees()))
                invalidChild2 = True
            elif (child2.height() < self.minHeight):
                invalidChild2 = True

            if not invalidChild1:
                self.fitnessFunction.evaluate(child1)
                offsprings.append(child1)
                
            if not invalidChild2:
                self.fitnessFunction.evaluate(child2)
                offsprings.append(child2)

        return offsprings
            


    def run(self):

        self.startTime = time.time()

        self.population = self.initialPopulation()
        
        while not self.stopCondition():

            individualsForReproduction = tournamentSelection(self.population, self.reproductionSize, self.tournamentSize)
            newGeneration = self.createGeneration(individualsForReproduction)
            self.population = newGeneration
            self.generations = self.generations + 1

            if self.verbose:
                print ('g:',self.generations,'best fitness:', np.round(self.fitnessFunction.elite.fitness,3), ', size:', len(self.fitnessFunction.elite.subtrees()))
            
            
