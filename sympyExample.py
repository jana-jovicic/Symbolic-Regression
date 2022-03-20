from ast import parse
import numpy as np
import sympy as sym
from sympy.parsing.sympy_parser import parse_expr

from expression import *


def main():

    X_set0 = np.array([[10,20,30]])
    X_set1 = np.array([[10,20,30], [40,50,60], [1,2,3]])

    x0 = VariableNode(0)
    x1 = VariableNode(1)
    x2 = VariableNode(2)
    print("x1 VariableNode", x1.stringRepresentation())

    x1Sympy = parse_expr(x1.stringRepresentation())
    print("x1Sympy",x1Sympy)

    ephConst1 = EphemeralRandomConstantNode()
    print("EphemeralRandomConstantNode", ephConst1.stringRepresentation())


    addNode = AddNode()
    addNode.appendLeft(x0)
    addNode.appendRight(x1)
    print("addNode", addNode.stringRepresentation())
    #print("addNode value", addNode.value(X_set1))
    #print("addNode value", addNode.value(X_set1))

    addNodeSympy = parse_expr(addNode.stringRepresentation())
    print("addNodeSympy", addNodeSympy)

    addNode2 = AddNode()
    addNode2.appendLeft(x1)
    addNode2.appendRight(x0)
    print("addNode2", addNode2.stringRepresentation())

    addNode2Sympy = parse_expr(addNode2.stringRepresentation())
    print("addNode2Sympy", addNode2Sympy)

    divNode =  DivNode()
    divNode.appendLeft(x2)
    divNode.appendRight(ephConst1)
    print("divNode", divNode.stringRepresentation())
    
    divNodeSympy = parse_expr(divNode.stringRepresentation())
    print("divNodeSympy", divNodeSympy)


    print()
    powNode = PowNode()
    powNode.appendLeft(x1)
    powNode.appendRight(ephConst1)
    powNodeSympy = parse_expr(powNode.stringRepresentation())
    print("powNode", powNode.stringRepresentation())
    print("powNodeSympy", powNodeSympy)


    """
    cosNode = CosNode()
    cosNode.appendLeft(x1)
    print(cosNode)
    print(cosNode.stringRepresentation())
    #print(cosNode.value(X_set1))


    divNode = DivNode()
    divNode.appendLeft(cosNode)
    divNode.appendRight(addNode)
    print(divNode.stringRepresentation())
    print(divNode.value(X_set1))
    """

    print()
   
    addNodesDiff1 = addNodeSympy - addNode2Sympy
    print("addNodesDiff1", addNodesDiff1)   
    addNodesDiff1Simplified = sym.simplify(addNodesDiff1)
    print("addNodesDiff1 simplified", addNodesDiff1Simplified)  
    print(addNodesDiff1Simplified == 0)

    addNodesDiff2 = addNode2Sympy - addNodeSympy
    print("addNodesDiff2", addNodesDiff2)   
    print("addNodesDiff2 simplified",sym.simplify(addNodesDiff2)) 

    addDivDiff1 = addNodeSympy - divNodeSympy
    print("addDivDiff1", addDivDiff1)   
    print("addDivDiff1 simplified",sym.simplify(addDivDiff1))  
    print(addDivDiff1 == 0)

if __name__ == "__main__":
    main()
