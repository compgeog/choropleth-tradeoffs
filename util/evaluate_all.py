import random
from .breakpoints import *
from .classify import *

def gvf(classes, data, numclass): # goodness of variance fit
    mean = float(sum(data))/len(data)
    indices = range(len(data))
    sum0 = 0
    for j in range(numclass):
        thisclass = [data[i] for i in range(len(data)) if classes[i]==j]
        lenthisclass = len(thisclass)
        if lenthisclass == 0:
            meani = 0
        else:
            meani = float(sum(thisclass))/lenthisclass
        sum0 += sum([(d-meani)*(d-meani) for d in thisclass])
    sum1 = sum([(d-mean)*(d-mean) for d in data])
    return 1-float(sum0)/sum1


def gvf2(classes, data, numclass): # goodness of variance fit, using list comprehensions
    class_counts = [ len([i for i in classes if i==j]) for j in range(numclass) ] 
    class_means = [ sum([data[i] for i in range(len(data)) if classes[i]==j])/float(class_counts[j]) for j in range(numclass) ]
    #means = [ class_means[i] for i in classes ]
    sum0 = sum([(data[i]-class_means[classes[i]])**2 for i in range(len(data))])
    mean = float(sum(data))/len(data)
    sum1 = sum([(d-mean)*(d-mean) for d in data])
    return 1-float(sum0)/sum1


def oai(classes, data, areas, numclass): # overview accuracy index
    class_counts = [ len([i for i in classes if i==j]) for j in range(numclass) ] 
    class_means = [ sum([data[i] for i in range(len(data)) if classes[i]==j])/float(class_counts[j]) for j in range(numclass) ]
    #means = [ class_means[i] for i in classes ]
    sum0 = sum([abs(data[i]-class_means[classes[i]])*areas[i] for i in range(len(data))])
    mean = float(sum(data))/len(data)
    sum1 = sum([abs(data[i]-mean)*areas[i] for i in range(len(data))])
    return 1-float(sum0)/sum1

def bai(shpadj, data, classes): # boundary accuracy index
    # boundary btw classes
    sum_h = sum([abs(data[b[0]]-data[b[1]]) for b in shpadj])
    # boundary btw original units
    sum_g = sum([abs(data[b[0]]-data[b[1]]) for b in shpadj if classes[b[0]]!=classes[b[1]]])
    return float(sum_g)/sum_h

