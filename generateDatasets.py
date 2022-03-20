import os
import argparse
import numpy as np

dir = 'generatedDatasets/'


def f1(numPoints):
    # f1 = x0**3 + x0**2 + x0

    filenameEquation = dir + 'f1_solution.txt'
    open(filenameEquation, 'w').close()
    with open(filenameEquation, 'w') as file:
        file.write('x0**3 + x0**2 + x0')

    filename = dir+'f1.txt'
    for i in range(numPoints):
        x = np.random.random()*2 - 1
        f = x**3 + x**2 + x
        #print(f)
        with open(filename, 'a+') as file:
            file.write(str(x)+' ')
            file.write(str(f))
            file.write('\n')


def f2(numPoints):

    filenameEquation = dir + 'f2_solution.txt'
    open(filenameEquation, 'w').close()
    with open(filenameEquation, 'w') as file:
        file.write('x0**2 + x1**2 + x2**2')

    filename = dir+'f2.txt'
    open(filename, 'w').close()
    for i in range(numPoints):
        x0 = np.random.random()*2 - 1
        x1 = np.random.random()*2 - 1
        x2 = np.random.random()*2 - 1
        f = x0**2 + x1**2 + x2**2
        #print(f)
        with open(filename, 'a+') as file:
            file.write(str(x0)+' ')
            file.write(str(x1)+' ')
            file.write(str(x2)+' ')
            file.write(str(f))
            file.write('\n')

def f3(numPoints):

    filenameEquation = dir + 'f3_solution.txt'
    open(filenameEquation, 'w').close()
    with open(filenameEquation, 'w') as file:
        file.write('x0**2 + x1**2')

    filename = dir+'f3.txt'
    open(filename, 'w').close()
    for i in range(numPoints):
        x0 = np.random.random()*2 - 1
        x1 = np.random.random()*2 - 1
        f = x0**2 + x1**2
        #print(f)
        with open(filename, 'a+') as file:
            file.write(str(x0)+' ')
            file.write(str(x1)+' ')
            file.write(str(f))
            file.write('\n')


nameFunctionMap = {"f1":f1, "f2":f2, "f3":f3}

def main():

    parser = argparse.ArgumentParser(description='create DL')
    parser.add_argument('--function', default='f1', type=str, help='function name (f1 - fn)')
    parser.add_argument('--numPoints', default='20', type=int, help='number of points (per function) to be generated')
    args = parser.parse_args()

    if not os.path.exists(dir):
      os.makedirs(dir)

    f = nameFunctionMap[args.function]
    f(args.numPoints)


if __name__ == "__main__":
    main()