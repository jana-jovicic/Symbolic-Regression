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
		maxTreeSize = 10,
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
        print("terminals", terminals)
        print(type(terminals))
       
        self.currentBestSolution = ''
        self.currentBestSolutionError = np.inf

        foundExactSolution = False
        exactSolution = ''
        exactSolutionErr = np.inf

        height = 0

        self.startTime = time.time()

        while True:

            
            print("height of the current trees: ", height)

            terminalPermutations = []
            for pair in itertools.product(terminals, repeat=2):
                terminalPermutations.append(pair)
                #print("pair:", pair[0].stringRepresentation(), ", ", pair[1].stringRepresentation())

            foundExactSolution, exactSolution, exactSolutionErr, functions, maxTimeExceeded = self.buildTree(terminalPermutations)

            if maxTimeExceeded:
                break 

            print('foundSolution', foundExactSolution)
            if foundExactSolution:
                print('solution', exactSolution.stringRepresentation())
                break
            #print('functions', functions)


            
            # -----------
            # just for debug
            height += 1
            #if height == 3:
                #break
            # ----------
            

            
            for function in functions:

                hours, rem = divmod(time.time() - self.startTime, 3600)
                #minutes, seconds = divmod(rem, 60)
                
                if hours >= self.maxHours:
                    break

                if any(terminal.stringRepresentation() == function.stringRepresentation() for terminal in terminals):
                    continue
                else:
                    terminals.append(deepcopy(function))
                   
                    

            #for term in terminals:
                #print("term", term.stringRepresentation())

            print("Generating permutations...")
            terminalPermutations = []
            for pair in itertools.product(terminals, repeat=2):
                terminalPermutations.append(pair)
            print("Finished Generating permutations")
            

            #for pair in terminalPermutations:
                #print("pair", pair[0].stringRepresentation(),  pair[1].stringRepresentation())


            #print('------------------')


        return foundExactSolution, exactSolution, exactSolutionErr, self.currentBestSolution, self.currentBestSolutionError
        
        


    
    def buildTree(self, terminalPermutations):

        functions = []

        foundExactSolution = False
        exactSolution = ''
        exactSolutionErr = np.inf

        for func in self.functions:
            #print(func)

            n = len(terminalPermutations)
            #for pair in terminalPermutations:
            for i in range(n):

                hours, rem = divmod(time.time() - self.startTime, 3600)
                minutes, _ = divmod(rem, 60)
                #print("minutes passed: ", minutes)
                if hours >= self.maxHours:
                    return False, '', '', functions, True

                pair = terminalPermutations[i]
                func.appendLeft(deepcopy(pair[0]))

                if func.arity == 1:
                    #print(pair)
                    #print(terminalPermutations[i-1])
                    if pair[0] == terminalPermutations[i-1][0]:
                        #print("same")
                        continue

                if func.arity > 1:
                    func.appendRight(deepcopy(pair[1]))
                #print(func.stringRepresentation())

                functions.append(deepcopy(func))

                yPred = func.value(self.X)
                yPred = [np.inf if np.isnan(y) else y for y in yPred]
                #print(y_pred[:5])
                err = self.mse(self.y, yPred)
                #print("mse", err)

                if err < self.currentBestSolutionError:
                    self.currentBestSolution = func
                    self.currentBestSolutionError = err

                    """
                    with open(self.csvFile, 'w', encoding='UTF8') as file:
                        writer = csv.writer(file)
                        writer.writerow(data)
                    """

                    self.updateResultsFile()
                    

                #print(self.currentBestSolution.stringRepresentation())
                #print(self.currentBestSolutionError)

                if err < self.errorEpsilon:
                    foundExactSolution = True
                    exactSolution = func
                    exactSolutionErr = err
                    #self.currentBestSolutionError = err
                    #self.currentBestSolution = func
                    break
            

            if foundExactSolution:
                break

        return foundExactSolution, exactSolution, exactSolutionErr, functions, False


    def updateResultsFile(self):

        """
        op = open(self.csvFile, "r")
        dt = csv.DictReader(op)
        up_dt = []

        executionTime = round(time.time()) - self.startTime
        hours, rem = divmod(executionTime, 3600)
        minutes, seconds = divmod(rem, 60)
        executionTimeFormated = '{:0>2}:{:0>2}:{:05.2f}'.format(int(hours), int(minutes), seconds)

        for r in dt:
            row = {
                'realEquation': r['realEquation'],
                'foundExactSolution': '/',
                'exactSolution': '/',
                'sympyEquivalence': '/',
                'nearestBestSolution': self.currentBestSolution,
                'nearestBestSolutionError': self.currentBestSolutionError,
                'Time (h:m:s)': executionTimeFormated,
                'maxGivenHours': self.maxHours}
            up_dt.append(row)

        print('up_dt', up_dt)
        op.close()
        op = open(self.csvFile, "w", newline='')
        headers = ['realEquation', 'foundExactSolution', 'exactSolution', 'sympyEquivalence', 'nearestBestSolution', 'nearestBestSolutionError', 'Time (h:m:s)', 'maxGivenHours']
        data = csv.DictWriter(op, delimiter=',', fieldnames=headers)
        data.writerow(dict((heads, heads) for heads in headers))
        data.writerows(up_dt)
        
        op.close()
        """

        """
        tempfile = NamedTemporaryFile(mode='w', delete=False)

        executionTime = round(time.time()) - self.startTime
        hours, rem = divmod(executionTime, 3600)
        minutes, seconds = divmod(rem, 60)
        executionTimeFormated = '{:0>2}:{:0>2}:{:05.2f}'.format(int(hours), int(minutes), seconds)

        header = ['realEquation', 'foundExactSolution', 'exactSolution', 'sympyEquivalence', 'nearestBestSolution', 'nearestBestSolutionError', 'Time (h:m:s)', 'maxGivenHours']

        with open(self.csvFile, 'r') as csvfile, tempfile:
            reader = csv.DictReader(csvfile, fieldnames=header)
            writer = csv.DictWriter(tempfile, fieldnames=header)
            for row in reader:
                row = {'realEquation': row['realEquation'], 'foundExactSolution': row['foundExactSolution'], 'exactSolution': row['exactSolution'], 'sympyEquivalence': row['sympyEquivalence'], 'nearestBestSolution': self.currentBestSolution.stringRepresentation(), 'nearestBestSolutionError': self.currentBestSolutionError, 'Time (h:m:s)': executionTimeFormated, 'maxGivenHours': self.maxHours}
                writer.writerow(row)

        shutil.move(tempfile.name, self.csvFile)
        """

        executionTime = round(time.time()) - self.startTime
        hours, rem = divmod(executionTime, 3600)
        minutes, seconds = divmod(rem, 60)
        executionTimeFormated = '{:0>2}:{:0>2}:{:05.2f}'.format(int(hours), int(minutes), seconds)
        
        with open(self.csvFile, 'r') as readFile:
            reader = csv.reader(readFile)
            lines = list(reader)
            lines[1][4], lines[1][5], lines[1][6], lines[1][7] = self.currentBestSolution.stringRepresentation(), self.currentBestSolutionError, executionTimeFormated, self.maxHours
            print(lines)
        
        with open(self.csvFile, 'w') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(lines)