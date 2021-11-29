from .breakpoints import *
from bisect import bisect_right

class _interval:
    def __init__(self, bounds=[]):
        if len(bounds) != 2:
            self.min, self.max = 0, 0
        else:
            self.min, self.max = bounds[0], bounds[1]
    def __repr__(self):
        return "{0} - {1}".format(self.min, self.max)
        self.max = max

class _interval_data(_interval):
    def __init__(self, brk1, brk2, data):
        if brk2>=len(data):
            brk2 = -1
        self.min = data[brk1+1] # brk1 starts from -1
        self.max = data[brk2]
    def __repr__(self):
        return "{0} - {1}".format(self.min, self.max)

class intervals:
    def __init__(self, is_integer = True):
        """
        data must be sorted
        is_integer is True if breakpoints are all integers
        """
        self.init = 0
        self.numclass = 0
        self.intervals = []
        self.lowers = []
        self.is_integer = is_integer

    def classify(self, data, numclass, method=1):
        self.numclass = numclass
        tmpintervals = classify(data, numclass, method=method)
        self.intervals = [_interval([tmpintervals[i], tmpintervals[i+1]]) for i in range(numclass)]
        self.lowers = [tmpintervals[i] for i in range(numclass)]
        self.init = 1

    def set_classes_by_data(self, brks, data):
        """
        data must be sorted
        """
        intvs = [-1] + [c.pos for c in brks.current] + [brks.n]
        self.numclass = brks.k + 1
        self.intervals = [_interval(self.find_bounds(intvs[i], intvs[i+1], data))
                          for i in range(self.numclass)]
        #self.intervals = [_interval_data(intvs[i], intvs[i+1], data) for i in range(self.numclass)]
        self.lowers = [i.min for i in self.intervals] # lower bounds
        self.init = 1

    def set_classes_by_data2(self, brks, data):
        """
        Similar to the above, except brks are ...
        data must be sorted
        """
        n = len(data)
        intvs = [-1] + brks + [n]
        self.numclass = len(brks) + 1
        self.intervals = [_interval(self.find_bounds(intvs[i], intvs[i+1], data))
                          for i in range(self.numclass)]
        #self.intervals = [_interval_data(intvs[i], intvs[i+1], data) for i in range(self.numclass)]
        self.lowers = [i.min for i in self.intervals] # lower bounds
        self.init = 1

    def find_bounds(self, brk1, brk2, data):
        """
        Finds the lower and upper bounds in data given two breakpoints brk1 and brk2
        and returns them in a list of [lower, upper]
        """
        if brk2>=len(data):
            brk2 = -1
        min = data[brk1+1] # brk1 starts from -1
        max = data[brk2]
        return [min, max]

    def set_classes(self, bounds):
        """
        Set the bounds without using the breakpoints
        The external call must take care of the correct bounds

        bounds: [ [lower, upper], [lower, upper], ... ]
        """
        self.numclass = len(bounds)
        self.intervals = [ _interval(b) for b in bounds ]
        self.lowers = [i.min for i in self.intervals] # lower bounds
        self.init = 1

    def get_class(self, val):
        i = bisect_right(self.lowers, val)            # leftmost lower bound that is greater than val
        if i>0:
            i = i-1
        return i

    def __repr__(self):
        return ", ".join(["[{0}]".format(i) for i in self.intervals])


def classify(val, numclass, method=1):
    """
    val: a list of values that determine the classification scheme
    numclass: number of classes
    method: 1 - quantile
            2 - equal interval
            3 - natural break
    Return: classes [ v1, v2, v3, ... vn+1 ]
            class 1:   v1 <= x < v2
            class 2:   v2 <= x < v3
            ...
            class n:   vn <= x < vn+1
    """
    val1 = sorted(val)
    n = len(val1)
    classes = [-1] * (numclass+1)
    classes[0] = val1[0]
    classes[-1] = val1[-1]+1
    if method==1:  # quantile
        nn = float(n)/numclass
        j = 0
        for i in range(1, n):
            if i >= (j+1)*nn:
                if val1[i] != classes[j]:
                    classes[j+1] = val1[i]
                    if j==numclass-2:
                        break
                    j += 1
    elif method==2:
        interval = float(max(val1)-min(val1))/numclass
        for i in range(1, numclass):
            classes[i] = i*interval
        pass
    return classes
