from copy import deepcopy
import time
import inspect
from GeneticProgramming.fitness import r2Score
from VNP.localSearch import ETT
from VNP.mutation import changeNodeValue, swapSubtree

from expression import *
from GeneticProgramming.randomTreeGenerator import generateRandomTree


class VNP:

    def __init__(
        self,
        terminals,
        functions = [AddNode(), SubNode(), MulNode(), DivNode()],
        minInitTreeDepth = 4,
        maxInitTreeDepth = 6,
        kMax = 500,
        maxIterations = 500,
        maxHours = 3,
        maxTreeDepth = 6):

        args, _, _, values = inspect.getargvalues(inspect.currentframe())
        values.pop('self')
        for arg, val in values.items():
            setattr(self, arg, val)

        #self.bestSolutionScore = -np.inf
        


    def stopCondition(self):
        terminate = False
        elapsedTime = time.time() - self.startTime
        hours, rem = divmod(elapsedTime, 3600)

        if self.bestSolutionScore == 1.0:
            terminate = True
        elif self.iteration > self.maxIterations:
            terminate = True
        elif self.maxHours > 0 and hours >= self.maxHours:
            terminate = True

        return terminate


    def shake(self, T, k, X, y):

        #neighborhoodTypes = [changeNodeValue(T, self.functions, self.terminals), swapSubtree(T, self.functions, self.terminals, X, self.maxInitTreeDepth, self.minInitTreeDepth)]
        #s = np.random.choice([0,1])
        #neighborhoodType = neighborhoodTypes[s]
        #print("neighborhoodType", str(neighborhoodType))

        neighborhoodTypes = ['changeNodeValue', 'swapSubtree']
        s = np.random.choice(neighborhoodTypes)

        for i in range(k):

            #newT = neighborhoodType(T)
            #newT = neighborhoodTypes[s]

            if s == 'changeNodeValue':
                newT = changeNodeValue(T, self.functions, self.terminals)
            elif s == 'swapSubtree':
                newT = swapSubtree(T, self.functions, self.terminals, X, self.maxInitTreeDepth, self.minInitTreeDepth)

            if not newT.isFeasible(X):
                continue

            #if self.maxTreeDepth > -1 and newT.height() > self.maxTreeDepth:
                #continue

            T = deepcopy(newT)

        return T


    def run(self, T, X, y):

        self.bestSolution = T
        self.bestSolutionScore = r2Score(y, T.value(X))

        self.iteration = 1
        self.startTime = time.time()

        while not self.stopCondition():

            for k in range(self.kMax):

                newT = self.shake(T, k, X, y)
                _, transformedT = ETT(newT, X, y)

                if not transformedT.isFeasible(X):
                    continue

                if self.maxTreeDepth > -1 and transformedT.height() > self.maxTreeDepth:
                    continue
                
                # Neighborhood change
                T = deepcopy(transformedT)

                y_pred = T.value(X)
                score = r2Score(y, y_pred)
                #print("score",score)
                if score > self.bestSolutionScore:
                    self.bestSolutionScore = score
                    self.bestSolution = deepcopy(T)
                    k = 0

                print("Iteration {0}: Best solution {1}, score {2}".format(self.iteration, self.bestSolution.stringRepresentation(), self.bestSolutionScore))
                

            self.iteration += 1

        


    def fit(self, X, y):

        T = generateRandomTree(self.functions, self.terminals, self.maxInitTreeDepth, currentHeight=0, 
                method='grow', minDepth=self.minInitTreeDepth)

        while not T.isFeasible(X):
            T = generateRandomTree(self.functions, self.terminals, self.maxInitTreeDepth, currentHeight=0, 
                method='grow', minDepth=self.minInitTreeDepth)

        self.run(T, X, y)

        y_pred = self.bestSolution.value(X)
        self.bestSolutionScore = r2Score(y, y_pred)



    def getBest(self):
        return self.bestSolution

    def getBestScore(self):
        return self.bestSolutionScore

    def predict(self, X):
        prediction = self.bestSolution.value(X)
        return prediction