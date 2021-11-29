# this one only uses the minimum part in onions.py to get the pareto ranking and dominating/dominated solutions.
#
# No visualization here
#

import sys

from osgeo import ogr
from gdalogr.adjacency_matrix import *

from gdalogr.getattr import *
from spatialanalysis.moransi2 import *

from copy import deepcopy
import random

#%matplotlib inline

from evaluate_all import *
from pareto_ranking import *


shpfname = 'data/newenglandcnty_att_prj_all_butter.shp'
attrname = 'Milk'
shpadj = adjacency_matrix(shpfname, output='L')

numclass = 4

val = get_shp_attribute_by_name(shpfname, attrname)
areas = get_shp_attribute_by_name(shpfname, 'AreaKM2')

m = len(val) # number of data
newval = list(set(val))
newval.sort()
n = len(newval)
print min(val), max(val)


# Now we iterate through all the break points.

# a nice solution from:
# http://stackoverflow.com/questions/127704/algorithm-to-return-all-combinations-of-k-elements-from-n
def choose_iter(elements, length):
    for i in xrange(len(elements)):
        if length == 1:
            yield (elements[i],)
        else:
            for next in choose_iter(elements[i+1:len(elements)], length-1):
                yield (elements[i],) + next


def choose(l, k):
    return list(choose_iter(l, k))

#mybrksitr = breakpoints(numclass-1, n-1)
mybrksitr = choose(range(n-1), numclass-1)
myint = intervals()
eval_results = []
allintervals = []
#while mybrksitr.next() is not None:
for brks in mybrksitr:
    myint.set_classes_by_data2(list(brks), newval)
    allintervals.append(deepcopy(myint))
    classes = [myint.get_class(i) for i in val]
    class_counts = [ len([i for i in classes if i==j]) for j in range(numclass) ] 
    class_means = [ sum([val[i] for i in range(m) if classes[i]==j])/float(class_counts[j])
                    for j in range(numclass) ]
    means = [ class_means[i] for i in classes ]
    #gvf(classes, val, numclass)
    o1 = gvf2(classes, val, numclass)
    o2 = oai(classes, val, areas, numclass)
    o3 = moransi2(means, shpadj)
    o4 = bai(shpadj, val, classes)
    eval_results.append([o1, o2, o3, o4])


# Pareto ranking all solutions.


evalranks = pareto_ranking(eval_results[:1000], minimize=False, verbose=True)
#evalranks = pareto_ranking(eval_results, minimize=False, verbose=True)

len(evalranks)
# 45760

# In this part, we evaluate the classification from the old paper.

#bounds = [ [0, 500], [500.001, 1000], [1000.001, 3000], [3000.001, 4000] ] # butter and cheese
#bounds = [ [0, 100], [100.001, 500], [500.001, 1000], [1000.001, 5000] ] # potatoes
#bounds = [ [0,1000], [1000.001, 5000], [5000.001, 25000], [25000.001, 100000], [100000.001, 5000000]] # for manufac.
bounds = [ [0,5000], [5000.001, 10000], [10000.001, 20000], [20000.001, 300000]] # for milk.

ref_int = intervals()
ref_int.set_classes(bounds)
ref_classes = [ref_int.get_class(i) for i in val]

class_counts = [ len([i for i in ref_classes if i==j]) for j in range(numclass) ] 
class_means = [ sum([val[i] for i in range(m) if ref_classes[i]==j])/float(class_counts[j]) for j in range(numclass) ]
sum0 = sum([(val[i]-class_means[ref_classes[i]])**2 for i in range(len(val))])
mean = float(sum(val))/len(val)
sum1 = sum([(d-mean)*(d-mean) for d in val])
1-float(sum0)/sum1

means = [ class_means[i] for i in ref_classes ] # for moran's I

o1 = gvf2(ref_classes, val, numclass)
o2 = oai(ref_classes, val, areas, numclass)
o3 = moransi2(means, shpadj)
o4 = bai(shpadj, val, ref_classes)
reference_result = [ o1, o2, o3, o4 ]


dominated = [eval_results[i] for i in range(len(evalranks)) if evalranks[i] <> 1 ]
nondominated = [eval_results[i] for i in range(len(evalranks)) if evalranks[i] == 1 ]
d,dominating_sols = is_dominated2(eval_results, reference_result, minimize=False, getall=True)


conclusion = 'There are {total} possible classifications, among which {nd} are non-dominated solutions and {dd} are dominated. The reference classification is dominated by {dt} solutions'.\
format(total= len(eval_results), dd=len(dominated), nd=len(nondominated), dt=len(dominating_sols))
print conclusion


# Below is the plot with the reference line, in red. Comparing two plots, we are
# convinced that the red line is dominated by the blue ones because otherwise we
# should see a darkgrey line in the place where the red line is.

bests = []
for i in range(4):
    os = [x[i] for x in eval_results]
    osmax = max(os)
    idx = os.index(osmax)
    bests.append(idx)



