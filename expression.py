from cmath import nan
import numpy as np


class Node:	

    def __init__(self):
        self.fitness = np.inf
        self.parent = None
        self.arity = 0
        self.left = None
        self.right = None

    def nodeType(self):
        raise NotImplementedError('nodeType() is not implemented for base class Node')

    def subtrees(self):
        result = []
        self.getSubtreesRecursive(result)
        return result

    def stringRepresentation(self):
        result = [ '' ]
        self.stringRepresentationRecursive(result)
        return result[0]


    def appendLeft(self, leftChild=None):
        self.left = leftChild
        leftChild.parent = self

    def appendRight(self, rightChild=None):
        self.right = rightChild
        rightChild.parent = self


    def detachChildNode(self, child):
        detached = ""
        if self.left == child:
            self.left = None
            detached = "left"
        elif self.right == child:
            self.right = None
            detached = "right"
        child.parent = None
        return detached


    def value(self, X):
        return None

    def depth(self):
        # from given node to root
        n = self
        d = 0
        while (n.parent):
            d = d+1
            n = n.parent
        return d

    def height(self):
        # from given node to maximaly distant leaf
        currDepth = self.depth()
        subtree = self.subtrees()
        leaves = [x for x in subtree if x.arity == 0]
        maxH = 0
        for l in leaves:
            d = l.depth()
            if d > maxH:
                maxH = d
        return maxH - currDepth
        

    def getSubtreesRecursive(self, result):
        result.append(self)
        if self.arity == 1:
            self.left.getSubtreesRecursive(result)
        elif self.arity == 2:
            self.left.getSubtreesRecursive(result)
            self.right.getSubtreesRecursive(result)
        return result


    def stringRepresentationRecursive(self, result):
        args = []
        if self.arity == 1:
            self.left.stringRepresentationRecursive(result)
            args.append(result[0])
        if self.arity == 2:
            self.left.stringRepresentationRecursive(result)
            args.append(result[0])
            self.right.stringRepresentationRecursive(result)
            args.append(result[0])
        
        result[0] = self.stringRepresentationSpecificNode(args)
        return result


    def stringRepresentationSpecificNode(self, args):
        raise NotImplementedError('stringRepresentationSpecificNode() is not implemented for base class Node')
    
    def isFeasible(self, X):
        values = self.value(X)
        #print('-------------')
        #print('values ', values)
        #print('type values ', type(values))
        #print('shape values ', values.shape)
        #print(values.shape == ())
        if values.shape == ():
            values = np.array([values])
            #print('values ', values)
        isInfeasible = any(np.isnan(v) for v in values) or any(v == float("inf") for v in values) or any(v == float("-inf") for v in values)
        return not isInfeasible


class VariableNode(Node):
    def __init__(self, id):
        super(VariableNode, self).__init__()
        self.id = id

    def __str__(self):
        return 'x'+str(self.id)    

    def __repr__(self):
        return 'x'+str(self.id)    

    def stringRepresentationSpecificNode(self, args):
        return 'x'+str(self.id)

    def value(self, X):
        return X[:,self.id]
    
    def nodeType(self):
        return 'terminal'


class EphemeralRandomConstantNode(Node):
    def __init__(self):
        super(EphemeralRandomConstantNode, self).__init__()
        # random number from [-1,1]
        self.valueNumber = np.round(np.random.random()*2 - 1, 3)

    def __str__(self):
        return str(self.valueNumber)    

    def __repr__(self):
        return str(self.valueNumber)   

    def stringRepresentationSpecificNode(self, args):
        return str(self.valueNumber)

    def value(self, X):
        return np.array(self.valueNumber)

    def nodeType(self):
        return 'terminal'




"""
-------------------------------------------------------
Binary operators
-------------------------------------------------------
"""

class AddNode(Node):

    def __init__(self):
        super(AddNode,self).__init__()
        self.arity = 2
        
    def __str__(self):
        return '+'
        
    def __repr__(self):
        return '+'

    def stringRepresentationSpecificNode(self, args):
        return '(' + args[0] + ' + ' + args[1] + ')'

    def value(self, X):
        valLeft = self.left.value(X)
        valRight = self.right.value(X)
        return valLeft + valRight

    def nodeType(self):
        return 'function'



class SubNode(Node):

    def __init__(self):
        super(SubNode,self).__init__()
        self.arity = 2

    def __str__(self):
        return '-'

    def __repr__(self):
        return '-'

    def stringRepresentationSpecificNode(self, args):
        return '(' + args[0] + ' - ' + args[1] + ')'

    def value(self, X):
        valLeft = self.left.value(X)
        valRight = self.right.value(X)
        return valLeft - valRight

    def nodeType(self):
        return 'function'


class MulNode(Node):

    def __init__(self):
        super(MulNode,self).__init__()
        self.arity = 2

    def __str__(self):
        return '*'

    def __repr__(self):
        return '*'

    def stringRepresentationSpecificNode(self, args):
        return '(' + args[0] + ' * ' + args[1] + ')'

    def value(self, X):
        valLeft = self.left.value(X)
        valRight = self.right.value(X)
        return np.multiply(valLeft, valRight)

    def nodeType(self):
        return 'function'


class DivNode(Node):

    def __init__(self):
        super(DivNode,self).__init__()
        self.arity = 2

    def __str__(self):
        return '/'

    def __repr__(self):
        return '/'

    def stringRepresentationSpecificNode(self, args):
        return '(' + args[0] + ' / ' + args[1] + ')'

    def value(self, X):
        valLeft = self.left.value(X)
        valRight = self.right.value(X)
        #valRight = np.where(valRight == 0, 0.000001, valRight)
        return valLeft / valRight
        
    def nodeType(self):
        return 'function'


class PowNode(Node):

    def __init__(self):
        super(PowNode, self).__init__()
        self.arity = 2

    def __str__(self):
        return '**'

    def __repr__(self):
        return '**'

    def stringRepresentationSpecificNode(self, args):
        return '(' + args[0] + '**(' + args[1] + '))'

    def value(self, X):
        valLeft = self.left.value(X)
        valRight = self.right.value(X)
        return valLeft ** valRight

    def nodeType(self):
        return 'function'


"""
-------------------------------------------------------
Unary operators
-------------------------------------------------------
"""

class SinNode(Node):

    def __init__(self):
        super(SinNode, self).__init__()
        self.arity = 1

    def __str__(self):
        return 'sin'

    def __repr__(self):
        return 'sin'

    def stringRepresentationSpecificNode(self, args):
        return 'sin(' + args[0] + ')'

    def value(self, X):
        valLeft = self.left.value(X)
        return np.sin(valLeft)

    def nodeType(self):
        return 'function'


class CosNode(Node):

    def __init__(self):
        super(CosNode, self).__init__()
        self.arity = 1

    def __str__(self):
        return 'cos'

    def __repr__(self):
        return 'cos'

    def stringRepresentationSpecificNode(self, args):
        return 'cos(' + args[0] + ')'

    def value(self, X):
        valLeft = self.left.value(X)
        return np.cos(valLeft)

    def nodeType(self):
        return 'function'


class LogNode(Node):

    def __init__(self):
        super(LogNode, self).__init__()
        self.arity = 1

    def __str__(self):
        return 'log'

    def __repr__(self):
        return 'log'

    def stringRepresentationSpecificNode(self, args):
        return 'log(' + args[0] + ')'

    def value(self, X):
        valLeft = self.left.value(X)
        valLeft = np.where(valLeft == 0, 0.000001, valLeft)
        return np.log(valLeft)

    def nodeType(self):
        return 'function'




class ExpNode(Node):

    def __init__(self):
        super(ExpNode, self).__init__()
        self.arity = 1

    def __str__(self):
        return 'exp'

    def __repr__(self):
        return 'exp'

    def stringRepresentationSpecificNode(self, args):
        return 'exp(' + args[0] + ')'

    def value(self, X):
        valLeft = self.left.value(X)
        return np.exp(valLeft)

    def nodeType(self):
        return 'function'
