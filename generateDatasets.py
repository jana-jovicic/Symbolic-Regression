import os
import argparse
import numpy as np

dir = 'generatedDatasets/'


def f1(numPoints):
    filename = dir+'f1.txt'
    open(filename, 'w').close()
    for i in range(numPoints):
        x = np.random.random()*2 - 1
        f = x**3 + x**2 + x
        #print(f)
        with open(filename, 'a+') as file:
            file.write(str(x)+' ')
            file.write(str(f))
            file.write('\n')


def f2(numPoints):
    filename = dir+'f2.txt'
    open(filename, 'w').close()
    for i in range(numPoints):
        x1 = np.random.random()*2 - 1
        x2 = np.random.random()*2 - 1
        x3 = np.random.random()*2 - 1
        f = x1**2 + x2**2 + x3**2
        #print(f)
        with open(filename, 'a+') as file:
            file.write(str(x1)+' ')
            file.write(str(x2)+' ')
            file.write(str(x3)+' ')
            file.write(str(f))
            file.write('\n')

def f3(numPoints):
    filename = dir+'f3.txt'
    open(filename, 'w').close()
    for i in range(numPoints):
        x1 = np.random.random()*2 - 1
        x2 = np.random.random()*2 - 1
        f = x1**2 + x2**2
        #print(f)
        with open(filename, 'a+') as file:
            file.write(str(x1)+' ')
            file.write(str(x2)+' ')
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