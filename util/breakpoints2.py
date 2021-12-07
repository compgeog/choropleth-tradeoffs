"""
Break point interator

This is version 2.0. The older version (breakpoints.py) should not be used anymore.

"""

__author__ = "Ningchuan Xiao <ncxiao@gmail.com>"

import sys
from random import sample

# a nice solution from:
# http://stackoverflow.com/questions/127704/algorithm-to-return-all-combinations-of-k-elements-from-n

def choose_iter(elements, length):
    for i in range(len(elements)):
        if length == 1:
            yield (elements[i],)
        else:
            for next in choose_iter(elements[i+1:len(elements)], length-1):
                yield (elements[i],) + next

# get a list of all unique non-repeating combinations
def choose(l, k):
    return list(choose_iter(l, k)) 

class intError(Exception):
    """Base class for exceptions in this module."""
    def __init__(self):
        print("Interval Error")
        sys.exit(1)
    
class _breakpoint:
    """
    Stores information for a break point. Keep track of the current position of
    the breakpoint (pos) and mininum and maximum position of the breakpoint. 
    """
    def __init__(self):
        self.pos = 0
        self.min = 0
        self.max = 0
    def __repr__(self):
        return "{0},{1},{2}".format(self.pos, self.min, self.max)

class Breakpoints:
    """
    This class iterates the combinations of k breakpoints amount n possible
    breakpoints. The calling program needs to make sure that the number of possible
    breakpoints (n) are correct. For example, if the data has M unique values, the
    total number of possible breakpoints will M-1, i.e. n = M-1.

    For selecting k from n possible breakpoint positions, the zero-th breakpoint
    can point to posistions ranging from zero to n-k, the 1-th breakpoint from 1
    to n-k+1, and so on. The inital positions of each of the k breakpoints are
    configured in the reset() function.

    Parameters
    ----------

    k                 : interger
                        number of breakpoints to choose (for an interval)
    n                 : integer
                        number of possible breakpoints in the data

    Attributes
    ----------

    k                 : interger
                        number of breakpoints to choose (for an interval)
    n                 : integer
                        number of possible breakpoints in the data
    pointer           : integer
                        the current position in all combinations, -1 initially
    true_total        : integer
                        total number of possible combinations (n choose k)
    current           : object of class _breakpoint
                        a breakpoint, consists of pos, min, and max

    Examples
    --------

    The following includes an example of returning all possible combinations of 
    2 breakpoints in 5 possible breakpoints.

    >>> from breakpoints import *
    >>> help(Breakpoints)
    >>> myint = Breakpoints(2, 5)
    >>> print myint.true_total
    10
    >>> while myint.next() is not None:
    ...     print myint
    ... 
    0,1
    0,2
    0,3
    0,4
    1,2
    1,3
    1,4
    2,3
    2,4
    3,4

    >>> import random
    >>> data = [random.randint(0, 100) for i in range(6)]
    >>> newdata = list(set(data))
    >>> len(data)
    6
    >>> len(newdata)
    6
    >>> newdata
    [33, 69, 78, 15, 57, 93]
    >>> while myint.next() is not None:
    ...     intvs = [-1] + [c.pos for c in myint.current] + [len(newdata)-1]
    ...     for i in range(len(intvs)-1):
    ...         slice = newdata[intvs[i]+1:intvs[i+1]+1]
    ...         print slice,
    ...     print
    ... 
    [33] [69] [78, 15, 57, 93]
    [33] [69, 78] [15, 57, 93]
    [33] [69, 78, 15] [57, 93]
    [33] [69, 78, 15, 57] [93]
    [33, 69] [78] [15, 57, 93]
    [33, 69] [78, 15] [57, 93]
    [33, 69] [78, 15, 57] [93]
    [33, 69, 78] [15] [57, 93]
    [33, 69, 78] [15, 57] [93]
    [33, 69, 78, 15] [57] [93]

    """

    def __init__(self, k, n):
        if n<k:
            raise intError()
        self.k = k                 # number of breakpoints
        self.n = n                 # number of possible breakpoints
        self.pointer = -1          # a pointer tracking the current position in all combinations
        self.true_total = 0        # theoretical total
        self.current = [_breakpoint() for i in range(k)]
        a = 1
        b = 1
        for i in range(k):
            a *= n-i
            b *= i+1
        self.true_total = a/b
        self.iter = choose(range(n), k)

    def reset(self):
        """Set all break points to their minimum position"""
        for i in range(self.k):
            self.current[i].pos = i
            self.current[i].min = i
            self.current[i].max = self.n-self.k+i
        self.pointer = 0

    def random(self):
        brks = sample(range(self.n), self.k)
        brks.sort()
        for i in range(self.k):
            self.current[i].pos = brks[i]
            self.current[i].min = i
            self.current[i].max = self.n-self.k+i
        self.pointer = 0 # this is arbitrary

    def next(self):
        if self.pointer == -1:
            self.reset()
            return 1
        if self.current[self.k-1].pos != self.current[self.k-1].max:
            self.current[self.k-1].pos += 1
        else:
            is_reachmax = True
            for i in range(self.k-1, -1, -1): # Find the first place that reaches max
                if self.current[i].pos != self.current[i].max:
                    self.current[i].pos += 1
                    for j in range(i+1, self.k):
                        self.current[j].pos = self.current[j-1].pos+1
                    is_reachmax = False
            if is_reachmax:
                self.pointer = -1
                return None # 0               # stop = true
        self.pointer += 1
        return 1

    def __repr__(self):
        #return "\n".join([str(c) for c in self.current])
        return ",".join([str(c.pos) for c in self.current])
    
def test():
    myint = Breakpoints(2, 5)
    print(myint.true_total)
    while myint.next() is not None:
        print(myint)

    import random
    data = [random.randint(0, 100) for i in range(7)]
    newdata = list(set(data))
    myint = Breakpoints(3, len(newdata)-1)
    print("Data:", newdata)
    while myint.next() is not None:
        intvs = [-1] + [c.pos for c in myint.current] + [myint.n]
        print(myint, end='') 
        for i in range(len(intvs)-1):
            slice = newdata[intvs[i]+1:intvs[i+1]+1]
            print(slice, end='')
        print()

if __name__ == "__main__":
    test()

    
