import numpy as np

from expression import *

def main():

    X_set0 = np.array([[10,20,30]])
    X_set1 = np.array([[10,20,30], [40,50,60]])


    x0 = VariableNode(0)
    x1 = VariableNode(1)
    x2 = VariableNode(2)
    print("VariableNode", x0)
    print("VariableNode", x1)
    print("VariableNode", x1.stringRepresentation())

    const1 = ConstantNode(5)
    print("ConstantNode", const1)
    print("ConstantNode", const1.stringRepresentation())

    print("x0 value", x0.value(X_set0))
    print("x0 value", x0.value(X_set1))
    print("const1 value", const1.value(X_set0))



    addNode = AddNode()
    addNode.appendLeft(x0)
    addNode.appendRight(x1)
    print("addNode", addNode.stringRepresentation())
    print("addNode value", addNode.value(X_set0))
    print("addNode value", addNode.value(X_set1))

    divNode0 =  DivNode()
    divNode0.appendLeft(x2)
    divNode0.appendRight(const1)
    print(divNode0.stringRepresentation())
    print(divNode0.value(X_set1))

    
    cosNode = CosNode()
    cosNode.appendLeft(x1)
    print(cosNode)
    print(cosNode.stringRepresentation())
    print(cosNode.value(X_set1))

    logNode = LogNode()
    logNode.appendLeft(const1)
    print(logNode.stringRepresentation())
    print(logNode.value(X_set1))

    divNode = DivNode()
    divNode.appendLeft(cosNode)
    divNode.appendRight(addNode)
    print(divNode.stringRepresentation())
    print(divNode.value(X_set1))

   
    print("divNode subtree")
    divSubtrees = divNode.subtrees()
    print(divSubtrees)
    for subtree in divSubtrees:
        print("subtree:", subtree)
        print("subtree string repr:", subtree.stringRepresentation())


    print("addNode subtree")
    addSubtrees = addNode.subtrees()
    print(addSubtrees)
    for subtree in addSubtrees:
        print(subtree)


    print()
    print("Depths:")
    print("divNode", divNode.depth())
    print("addNode", addNode.depth())
    print("cosNode", cosNode.depth())
    print("x0", x0.depth())
    print("divNode0", divNode0.depth())
    print("const1", const1.depth())

    print()
    print("Heights:")
    print("divNode", divNode.height())
    print("addNode", addNode.height())
    print("cosNode", cosNode.height())
    print("x0", x0.height())
    print("divNode0", divNode0.height())
    print("const1", const1.height())


    print()
    print("Detaching addNode from divNode")
    print("divNode left", divNode.left)
    print("divNode right", divNode.right)
    print("addNode parent", addNode.parent)
    #print("divNode height", divNode.height())
    print("divNode depth", divNode.depth())
    detached = divNode.detachChildNode(addNode)
    print(detached)
    print(divNode)
    print("divNode left", divNode.left)
    print("divNode right", divNode.right)
    print("addNode parent", addNode.parent)
    #print("divNode height", divNode.height())
    print("divNode depth", divNode.depth())



if __name__ == "__main__":
    main()