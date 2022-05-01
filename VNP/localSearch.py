from copy import deepcopy
import numpy as np

def EET(initialTree):

    T = deepcopy(initialTree)
    #newTree = deepcopy(T)

    functionNodes = []
    terminalNodes = []

    subtreesT = T.subtrees()
    print("subtrees", subtreesT)

    for subtree in subtreesT:
        if subtree.nodeType() == 'function':
            functionNodes.append(subtree)
        if subtree.nodeType() == 'terminal':
            terminalNodes.append(subtree)


    FH = functionNodes + terminalNodes
    #print(FH)

    #for i in functionNodes:

    for k in range(len(functionNodes)):
        
        i = functionNodes[k]
        
        print("---------")
        
        print("i:", i)
        #print("parent(i): ", i.parent)
        #print("leftChild(i): ", i.left)
        #print("rightChild(i): ", i.right)
        
        
        #for j in FH:

        for m in range(len(FH)):

            j = FH[m]


            #print("T", T.stringRepresentation())
            print("j: ", j)
            #print(j == i.parent)
            if j == i or j == i.parent or j == i.left or j == i.right:  # or i == j.parent or i == j.left or i == j.right:
                        
                #print("True")
                continue

            #print("Adding new edge ({0}, {1})".format(i,j))

            if j.nodeType() == 'function':
                # case 1
                print("Adding new edge ({0}, {1})".format(i,j))

                x = np.random.choice([i, j])
                print('x', x)

                b = x.parent
                print("b", b)

                if x == i:
                    print("x == i")
                else:
                    print("x != i")

                    iChildren = []
                    if i.left is not None:
                        iChildren.append(i.left)
                    if i.right is not None:
                        iChildren.append(i.right)

                    iChild = np.random.choice(iChildren)

                    # remove (b, x) edge, where b is parent and x is child
                    bDetachedChildPosition = b.detachChildNode(x)
                    print("removing edge ({0}, {1})".format(b,x)) 

                    # remove (i, iChild) edge
                    iDetachedChildPosition = i.detachChildNode(iChild)
                    print("removing edge ({0}, {1})".format(i,iChild)) 

                    # add (i, x) edge, where i is parent
                    if iDetachedChildPosition == "left":
                        i.appendLeft(x)
                    elif iDetachedChildPosition == "right":
                        i.appendRight(x)
                    print("adding edge ({0}, {1}) on {2}".format(i, x, iDetachedChildPosition)) 
                        
                    # add (b, iChild) edge, where b is parent
                    if bDetachedChildPosition == "left":
                        b.appendLeft(iChild)
                    elif bDetachedChildPosition == "right":
                        b.appendRight(iChild)
                    print("adding edge ({0}, {1}) on {2}".format(b, iChild, bDetachedChildPosition)) 


                    newTree = deepcopy(T)
                    print("newTree", newTree.stringRepresentation())
                    #print("initialTree", initialTree.stringRepresentation())
                    
                    T = deepcopy(initialTree)
                    functionNodes = []
                    terminalNodes = []

                    subtreesT = T.subtrees()
                    print("subtrees", subtreesT)

                    for subtree in subtreesT:
                        if subtree.nodeType() == 'function':
                            functionNodes.append(subtree)
                        if subtree.nodeType() == 'terminal':
                            terminalNodes.append(subtree)


                    FH = functionNodes + terminalNodes

            """
            elif j.nodeType() == 'terminal':

                iChildren = []
                if i.left is not None:
                    iChildren.append(i.left)
                if i.right is not None:
                    iChildren.append(i.right)

                iChild = np.random.choice(iChildren)

                # remove (b, x) edge, where b is parent and x is child
                bDetachedChildPosition = b.detachChildNode(x)
                print("removing edge ({0}, {1})".format(b,x)) 

                # remove (i, iChild) edge
                iDetachedChildPosition = i.detachChildNode(iChild)
                print("removing edge ({0}, {1})".format(i,iChild)) 

                # add (i, x) edge, where i is parent
                if iDetachedChildPosition == "left":
                    i.appendLeft(x)
                elif iDetachedChildPosition == "right":
                    i.appendRight(x)

                print("adding edge ({0}, {1}) on {2}".format(i, x, iDetachedChildPosition)) 
                    
                # add (b, iChild) edge, where b is parent
                if bDetachedChildPosition == "left":
                    b.appendLeft(iChild)
                elif bDetachedChildPosition == "right":
                    b.appendRight(iChild)

                print("adding edge ({0}, {1}) on {2}".format(b, iChild, bDetachedChildPosition)) 


                newTree = deepcopy(T)
                print("newTree", newTree.stringRepresentation())
                print("initialTree", initialTree.stringRepresentation())

            """