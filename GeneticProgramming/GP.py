import inspect
from GeneticProgramming.crossover import SSC, subtreeCrossover
from GeneticProgramming.fitness import adjustedFitness
from GeneticProgramming.mutation import subtreeMutation, onePointMutation
from GeneticProgramming.randomTreeGenerator import generateRandomTree
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
        minDepth = 2,
        initializationMaxTreeDepth = 4,
        maxTreeSize = 10,
        tournamentSize = 4,
        reproductionSize = 200,
        fitnessType = 'mse',
        errorEpsilon = 1e-10,
        verbose = False,
        useSSC = False,
        sscLBSS = 1e-4,
		sscUBSS = 0.4,
		sscMaxTrials = 10):

        args, _, _, values = inspect.getargvalues(inspect.currentframe())
        values.pop('self')
        for arg, val in values.items():
            setattr(self, arg, val)

        self.population = []
        self.generations = 0


    def stopCondition(self):
        terminate = False
        elapsedTime = time.time() - self.startTime
        hours, rem = divmod(elapsedTime, 3600)
        
        if self.fitnessType == 'adjusted' or self.fitnessType == 'normalizedAdjusted':
            if self.fitnessFunction.bestIndividual.fitness > 0.9:
                terminate = True
                print("found best solution")
                print("fitness", self.fitnessFunction.bestIndividual.fitness)

        else:
            if self.fitnessFunction.bestIndividual.fitness < self.errorEpsilon:
                terminate = True


        if self.maxEvaluations > 0 and self.fitnessFunction.evaluations >= self.maxEvaluations:
            terminate = True
        elif self.maxGenerations > 0 and self.generations >= self.maxGenerations:
            terminate = True
        elif self.maxTime > 0 and hours >= self.maxTime:
            terminate = True

        if terminate and self.verbose:
            print('Terminating at\n\t', self.generations, 'generations\n\t', self.fitnessFunction.evaluations, 'evaluations\n\t', np.round(elapsedTime,2), 'seconds')

        return terminate


    def initialPopulation(self):

        population = []
        curretMaxDepth = self.minDepth
        initDepthInterval = self.populationSize / (self.initializationMaxTreeDepth - self.minDepth + 1)
        nextDepthInterval = initDepthInterval

        for i in range(self.populationSize):
            if i >= nextDepthInterval:
                nextDepthInterval += initDepthInterval
                curretMaxDepth += 1

            t = generateRandomTree(self.functions, self.terminals, curretMaxDepth, currentHeight=0, 
                method='grow' if np.random.random() < 0.5 else 'full', minDepth=self.minDepth)

            
            while not t.isFeasible(self.fitnessFunction.X_train):
                t = generateRandomTree(self.functions, self.terminals, curretMaxDepth, currentHeight=0, 
                method='grow' if np.random.random() < 0.5 else 'full', minDepth=self.minDepth)
            

            self.fitnessFunction.evaluate(t)

            population.append(t)
        
        return population


    def createGeneration(self, individualsForReproduction):

        offsprings = []
        while len(offsprings) < self.populationSize:

            invalidChild1 = False
            invalidChild2 = False

            parents = np.random.choice(individualsForReproduction, 2)

            if self.useSSC:
                child1, child2 = SSC(parents[0], parents[1], self.fitnessFunction.X_train, self.sscLBSS, self.sscUBSS, self.sscMaxTrials)
            else:
                child1, child2 = subtreeCrossover(parents[0], parents[1])
                
            if not child1.isFeasible(self.fitnessFunction.X_train):
                invalidChild1 = True
            if not child2.isFeasible(self.fitnessFunction.X_train):
                invalidChild2 = True
                

            # perform each type of mutation with equal opportunity
            if random() < 0.5:
                if random() < self.mutationRate:
                    child1 = subtreeMutation(child1, self.functions, self.terminals, self.fitnessFunction.X_train, maxHeight=self.initializationMaxTreeDepth, minDepth=self.minDepth)
                if random() < self.mutationRate:
                    child2 = subtreeMutation(child2, self.functions, self.terminals, self.fitnessFunction.X_train, maxHeight=self.initializationMaxTreeDepth, minDepth=self.minDepth)
            else:
                if random() < self.opMutationRate:
                    child1 = onePointMutation(child1, self.functions, self.terminals)
                    
                    if not child1.isFeasible(self.fitnessFunction.X_train):
                        invalidChild1 = True
                    
                if random() < self.opMutationRate:
                    child2 = onePointMutation(child2, self.functions, self.terminals)
                    
                    if not child2.isFeasible(self.fitnessFunction.X_train):
                        invalidChild2 = True
                    

            
            # check if children meet constraints	
            
            if self.maxTreeSize > -1 and len(child1.subtrees()) > self.maxTreeSize:
                invalidChild1 = True
            elif (child1.height() < self.minDepth):
                invalidChild1 = True

            
            if self.maxTreeSize > -1 and len(child2.subtrees()) > self.maxTreeSize:
                invalidChild2 = True
            elif (child2.height() < self.minDepth):
                invalidChild2 = True

            if not invalidChild1:
                self.fitnessFunction.evaluate(child1)
                offsprings.append(child1)
            else:
                offsprings.append(deepcopy(parents[0]))
                
            if not invalidChild2:
                self.fitnessFunction.evaluate(child2)
                offsprings.append(child2)
            else:
                offsprings.append(deepcopy(parents[1]))

        return offsprings
            


    def run(self):

        self.startTime = time.time()

        self.population = self.initialPopulation()
        
        if self.fitnessType == 'normalizedAdjusted':
            self.fitnessFunction.sumAdjustedFitnesses = self.calculateSumOfAdjustedFitnesses(self.population)
        
        while not self.stopCondition():

            individualsForReproduction = tournamentSelection(self.population, self.reproductionSize, self.tournamentSize)
            newGeneration = self.createGeneration(individualsForReproduction)
            self.population = newGeneration
            self.generations = self.generations + 1

            if self.fitnessType == 'normalizedAdjusted':
                self.fitnessFunction.sumAdjustedFitnesses = self.calculateSumOfAdjustedFitnesses(self.population)

            if self.verbose:
                print ('g:',self.generations,'best fitness:',self.fitnessFunction.bestIndividual.fitness, ', size:', len(self.fitnessFunction.bestIndividual.subtrees()))
            
            
    def calculateSumOfAdjustedFitnesses(self, population):
        sumAdjFit = 0
        for individual in population:
            sumAdjFit = sumAdjFit + adjustedFitness(self.fitnessFunction.y_train, individual.value(self.fitnessFunction.X_train))
        return sumAdjFit