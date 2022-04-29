import os
import argparse
import numpy as np

dir = 'generatedDatasets/'


def f1(numPoints):
    # f1 = x**3 + x**2 + x

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
    # f2 = x**4 + x**3 + x**2 + x

    filenameEquation = dir + 'f2_solution.txt'
    open(filenameEquation, 'w').close()
    with open(filenameEquation, 'w') as file:
        file.write('x0**4 + x0**3 + x0**2 + x0')

    filename = dir+'f2.txt'
    for i in range(numPoints):
        x = np.random.random()*2 - 1
        f = x**4 + x**3 + x**2 + x
        #print(f)
        with open(filename, 'a+') as file:
            file.write(str(x)+' ')
            file.write(str(f))
            file.write('\n')

def f3(numPoints):
    # f3 = x**5 + x**4 + x**3 + x**2 + x

    filenameEquation = dir + 'f3_solution.txt'
    open(filenameEquation, 'w').close()
    with open(filenameEquation, 'w') as file:
        file.write('x0**5 + x0**4 + x0**3 + x0**2 + x0')

    filename = dir+'f3.txt'
    for i in range(numPoints):
        x = np.random.random()*2 - 1
        f = x**5 +x**4 + x**3 + x**2 + x
        #print(f)
        with open(filename, 'a+') as file:
            file.write(str(x)+' ')
            file.write(str(f))
            file.write('\n')

def f4(numPoints):
    # f4 = x**6 + x**5 + x**4 + x**3 + x**2 + x

    filenameEquation = dir + 'f4_solution.txt'
    open(filenameEquation, 'w').close()
    with open(filenameEquation, 'w') as file:
        file.write('x0**6 + x0**5 + x0**4 + x0**3 + x0**2 + x0')

    filename = dir+'f4.txt'
    for i in range(numPoints):
        x = np.random.random()*2 - 1
        f = x**6 + x**5 +x**4 + x**3 + x**2 + x
        #print(f)
        with open(filename, 'a+') as file:
            file.write(str(x)+' ')
            file.write(str(f))
            file.write('\n')

def f5(numPoints):
    # f5 = sin(x ** 2) * cos(x) - 1

    filenameEquation = dir + 'f5_solution.txt'
    open(filenameEquation, 'w').close()
    with open(filenameEquation, 'w') as file:
        file.write('sin(x0 ** 2) * cos(x0) - 1')

    filename = dir+'f5.txt'
    for i in range(numPoints):
        x = np.random.random()*2 - 1
        f = np.sin(x**2) * np.cos(x) - 1
        with open(filename, 'a+') as file:
            file.write(str(x)+' ')
            file.write(str(f))
            file.write('\n')


def f6(numPoints):
    # f6 = sin(x) + sin(x + x**2)

    filenameEquation = dir + 'f6_solution.txt'
    open(filenameEquation, 'w').close()
    with open(filenameEquation, 'w') as file:
        file.write('sin(x0) + sin(x0 + x0**2)')

    filename = dir+'f6.txt'
    for i in range(numPoints):
        x = np.random.random()*2 - 1
        f = np.sin(x) + np.sin(x + x**2 )
        with open(filename, 'a+') as file:
            file.write(str(x)+' ')
            file.write(str(f))
            file.write('\n')

def f7(numPoints):
    # f7 = log(x + 1) + log(x**2 + 1)

    filenameEquation = dir + 'f7_solution.txt'
    open(filenameEquation, 'w').close()
    with open(filenameEquation, 'w') as file:
        file.write('log(x0 + 1) + log(x0**2 + 1)')

    filename = dir+'f7.txt'
    for i in range(numPoints):
        # x from [0,2]
        x = np.random.random()*2
        f = np.log(x + 1) + np.log(x**2 + 1)
        with open(filename, 'a+') as file:
            file.write(str(x)+' ')
            file.write(str(f))
            file.write('\n')

def f8(numPoints):
    # f8 = √x

    filenameEquation = dir + 'f8_solution.txt'
    open(filenameEquation, 'w').close()
    with open(filenameEquation, 'w') as file:
        file.write('√x0')

    filename = dir+'f8.txt'
    for i in range(numPoints):
        # x from [0,4]
        x = np.random.random()*4
        f = np.sqrt(x)
        with open(filename, 'a+') as file:
            file.write(str(x)+' ')
            file.write(str(f))
            file.write('\n')

def f9(numPoints):
    # f9 = sin(x0) + sin(x1 ** 2)

    filenameEquation = dir + 'f9_solution.txt'
    open(filenameEquation, 'w').close()
    with open(filenameEquation, 'w') as file:
        file.write('sin(x0) + sin(x1 ** 2)')

    filename = dir+'f9.txt'
    for i in range(numPoints):
        # points from [-1,1]
        x0 = np.random.random()*2 - 1
        x1 = np.random.random()*2 - 1
        f = np.sin(x0) + np.sin(x1 ** 2)
        with open(filename, 'a+') as file:
            file.write(str(x0)+' ')
            file.write(str(x1)+' ')
            file.write(str(f))
            file.write('\n')

def f10(numPoints):
    # f10 = 2sin(x0)cos(x1)

    filenameEquation = dir + 'f10_solution.txt'
    open(filenameEquation, 'w').close()
    with open(filenameEquation, 'w') as file:
        file.write('2 * sin(x0) * cos(x1)')

    filename = dir+'f10.txt'
    for i in range(numPoints):
        # points from [-1,1]
        x0 = np.random.random()*2 - 1
        x1 = np.random.random()*2 - 1
        f = 2 * np.sin(x0) * np.cos(x1)
        with open(filename, 'a+') as file:
            file.write(str(x0)+' ')
            file.write(str(x1)+' ')
            file.write(str(f))
            file.write('\n')


def f01(numPoints):
    # f01 = x0*x1 + x1

    filenameEquation = dir + 'f01_solution.txt'
    open(filenameEquation, 'w').close()
    with open(filenameEquation, 'w') as file:
        file.write('x0*x1 + x1')
    filename = dir+'f01.txt'
    for i in range(numPoints):
        x0 = np.random.random()*2 - 1
        x1 = np.random.random()*2 - 1
        f = x0*x1 + x1
        #print(f)
        with open(filename, 'a+') as file:
            file.write(str(x0)+' ')
            file.write(str(x1)+' ')
            file.write(str(f))
            file.write('\n')

def f02(numPoints):
    # f02 = x0*x1 + x1**2 + x0
    
    filenameEquation = dir + 'f02_solution.txt'
    open(filenameEquation, 'w').close()
    with open(filenameEquation, 'w') as file:
        file.write('x0*x1 + x1**2 + x0')
    filename = dir+'f02.txt'
    for i in range(numPoints):
        x0 = np.random.random()*2 - 1
        x1 = np.random.random()*2 - 1
        f = x0*x1 + x1**2 + x0
        #print(f)
        with open(filename, 'a+') as file:
            file.write(str(x0)+' ')
            file.write(str(x1)+' ')
            file.write(str(f))
            file.write('\n')

def f03(numPoints):
    # f03 = x0*x1 + cos(x0) + x1
    
    filenameEquation = dir + 'f03_solution.txt'
    open(filenameEquation, 'w').close()
    with open(filenameEquation, 'w') as file:
        file.write('x0*x1 + cos(x0) + x1')
    filename = dir+'f03.txt'
    for i in range(numPoints):
        x0 = np.random.random()*2 - 1
        x1 = np.random.random()*2 - 1
        f = x0*x1 + np.cos(x0) + x1
        #print(f)
        with open(filename, 'a+') as file:
            file.write(str(x0)+' ')
            file.write(str(x1)+' ')
            file.write(str(f))
            file.write('\n')


def f09(numPoints):
    # f09 = x0 + sin(x1)

    filenameEquation = dir + 'f09_solution.txt'
    open(filenameEquation, 'w').close()
    with open(filenameEquation, 'w') as file:
        file.write('x0 + sin(x1)')
    filename = dir+'f09.txt'
    for i in range(numPoints):
        x0 = np.random.random()*2 - 1
        x1 = np.random.random()*2 - 1
        f = x0 + np.sin(x1)
        #print(f)
        with open(filename, 'a+') as file:
            file.write(str(x0)+' ')
            file.write(str(x1)+' ')
            file.write(str(f))
            file.write('\n')

"""
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
"""

nameFunctionMap = {"f1":f1, "f2":f2, "f3":f3, "f4":f4, "f5":f5, "f6":f6, "f7":f7, "f8":f8, "f9":f9, "f10":f10, "f01":f01, "f02":f02, "f03":f03}

def main():

    parser = argparse.ArgumentParser(description='create dataset')
    parser.add_argument('--function', default='f1', type=str, help='function name (f1 - fn)')
    parser.add_argument('--numPoints', default='30', type=int, help='number of points (per function) to be generated')
    args = parser.parse_args()

    if not os.path.exists(dir):
      os.makedirs(dir)

    f = nameFunctionMap[args.function]
    f(args.numPoints)


if __name__ == "__main__":
    main()