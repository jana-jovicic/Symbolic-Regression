import time
import inspect
from VNP.localSearch import ETT

from expression import *
from GeneticProgramming.randomTreeGenerator import generateRandomTree


class VNP:

    def __init__(
        self,
        X,
        y,
        terminals,
        functions = [AddNode(), SubNode(), MulNode(), DivNode()],
        minDepth = 4,
        maxDepth = 10,
        kMax = 500,
        maxIterations = 500,
        maxHours = 3):

        args, _, _, values = inspect.getargvalues(inspect.currentframe())
        values.pop('self')
        for arg, val in values.items():
            setattr(self, arg, val)

        iteration = 0


    def stopCondition(self):
        terminate = False
        elapsedTime = time.time() - self.startTime
        hours, rem = divmod(elapsedTime, 3600)

        if self.iteration > self.maxIterations:
            terminate = True
        elif self.maxHours > 0 and hours >= self.maxHours:
            terminate = True

        return terminate


    def shake(T, k):
        pass


    def run(self):

        T = generateRandomTree(self.functions, self.terminals, self.maxDepth, currentHeight=0, 
                method='grow' if np.random.random() < 0.5 else 'full', minDepth=self.minDepth)

        while not self.stopCondition():

            for k in range(self.kMax):

                newT = self.shake(T, k)
                _, transformedT = ETT(newT, self.X, self.y)
                
                # Neighborhood_change