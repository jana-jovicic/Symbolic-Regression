import csv
import shutil
from tempfile import NamedTemporaryFile
import time
import inspect
import itertools
import numpy as np
from copy import deepcopy

from expression import *



class BruteForce():

    def __init__(self,
        X,
        y,
		functions = [AddNode(), SubNode(), MulNode(), DivNode(), LogNode()],
		errorType = 'mse',
		errorEpsilon = 1e-10,
        maxHours = 2,
        csvFile = './BruteForce/results/results.csv'):

        args, _, _, values = inspect.getargvalues(inspect.currentframe())
        values.pop('self')
        for arg, val in values.items():
            setattr(self, arg, val)


    def mse(self, y_real, y_pred):
        return np.mean(np.square(y_real - y_pred))


    def run(self):

        terminals = []
        nVariables = self.X.shape[1]
        for i in range(nVariables):
            terminals.append(VariableNode(i))
        #print("terminals", terminals)
        
        self.currentBestSolution = ''
        self.currentBestSolutionError = np.inf

        foundExactSolution = False
        exactSolution = ''
        exactSolutionErr = np.inf

        height = 0

        self.startTime = time.time()

        terminalPermutations = []
        for pair in itertools.product(terminals, repeat=2):
            print(pair[0].stringRepresentation(), pair[1].stringRepresentation())
            terminalPermutations.append(pair)

        while True:
            
            print("height of the current trees: ", height)

            foundExactSolution, exactSolution, exactSolutionErr, functions, maxTimeExceeded = self.buildTree(terminalPermutations)

            if maxTimeExceeded:
                break 

            #print('foundSolution', foundExactSolution)
            if foundExactSolution:
                #print('solution', exactSolution.stringRepresentation())
                break
            
            # -----------
            # just for debug
            height += 1
            #if height == 3:
                #break
            # ----------
            

            
            for function in functions:

                hours, rem = divmod(time.time() - self.startTime, 3600)
                
                if hours >= self.maxHours:
                    break

                if any(terminal.stringRepresentation() == function.stringRepresentation() for terminal in terminals):
                    #print("has terminal", function.stringRepresentation())
                    continue
                else:
                    terminals.append(deepcopy(function))
            
            
            print("Generating permutations...")
            terminalPermutations = []
            for pair in itertools.product(terminals, repeat=2):
                terminalPermutations.append(pair)
            print("Finished Generating permutations")


        return foundExactSolution, exactSolution, exactSolutionErr, self.currentBestSolution, self.currentBestSolutionError
        
        


    
    def buildTree(self, terminalPermutations):

        generatedFunctions = []
        foundExactSolution = False
        exactSolution = ''
        exactSolutionErr = np.inf

        for func in self.functions:

            n = len(terminalPermutations)
            for i in range(n):

                hours, rem = divmod(time.time() - self.startTime, 3600)
                minutes, _ = divmod(rem, 60)
                #print("minutes passed: ", minutes)
                if hours >= self.maxHours:
                    return False, '', '', generatedFunctions, True

                pair = terminalPermutations[i]

                if func.arity == 1:
                    if pair[0] == terminalPermutations[i-1][0]:
                        # This function was already used as root functions left child in previous iteration, no need to check it again.
                        # It can be done like this because of the way permutation pais are formed 
                        #print("same")
                        continue

                func.appendLeft(deepcopy(pair[0]))

                if func.arity > 1:
                    func.appendRight(deepcopy(pair[1]))
                #print("func", func.stringRepresentation())

                generatedFunctions.append(deepcopy(func))

                yPred = func.value(self.X)
                yPred = [np.inf if np.isnan(y) else y for y in yPred]
                err = self.mse(self.y, yPred)

                if err < self.currentBestSolutionError:
                    self.currentBestSolution = func
                    self.currentBestSolutionError = err

                    self.updateResultsFile()
                    


                if err < self.errorEpsilon:
                    foundExactSolution = True
                    exactSolution = func
                    exactSolutionErr = err
                    break
            

            if foundExactSolution:
                break

        return foundExactSolution, exactSolution, exactSolutionErr, generatedFunctions, False


    def updateResultsFile(self):

        executionTime = round(time.time()) - self.startTime
        hours, rem = divmod(executionTime, 3600)
        minutes, seconds = divmod(rem, 60)
        executionTimeFormated = '{:0>2}:{:0>2}:{:05.2f}'.format(int(hours), int(minutes), seconds)
        
        with open(self.csvFile, 'r') as readFile:
            reader = csv.reader(readFile)
            lines = list(reader)
            lines[1][4], lines[1][5], lines[1][6], lines[1][7] = self.currentBestSolution.stringRepresentation(), self.currentBestSolutionError, executionTimeFormated, self.maxHours
            
        with open(self.csvFile, 'w') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(lines)