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
        print(f)
        with open(filename, 'a+') as file:
            file.write(str(x)+' ')
            file.write(str(f))
            file.write('\n')


nameFunctionMap = {"f1":f1}

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