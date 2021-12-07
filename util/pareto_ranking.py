import sys

def is_better(v1, v2, minimize = True):
    """v1 dominiates (is better) v2 if v1 < v2 for minimizing"""
    if minimize:
        return v1 < v2
    else:
        return v1 > v2

def is_dominated(objs, ix, ranks, curr_rank, minimize=True): # pop stores the objs 
    ov1 = objs[ix]
    for i in range(len(objs)):
        if i==ix:
            continue
        a_rank = ranks[i]
        if a_rank and a_rank < curr_rank:
            continue
        ov2 = objs[i]
        k1, k2, k3 = 0, 0, 0
        for j in range(len(objs[0])):
            if is_better(ov1[j], ov2[j], minimize): # ov1[j] < ov2[j]:
                k1 += 1
            elif ov1[j] == ov2[j]:
                k2 += 1
            else:
                k3 += 1
        if k1==0 and k3>0:
            return True
    return False

def finding_nondominated(objs, minimize=True, verbose=False):
    """return the id's of items that are nondominated"""
    dominated = [0 for i in range(len(objs))]
    checked = [0 for i in range(len(objs))]
    nondominated = [0 for i in range(len(objs))]
    for i in range(len(objs)):
        if not is_dominated(objs, i, ranks, curr_rank, minimize):
            ranks[i] = curr_rank
            remain -= 1

def pareto_ranking(objs, minimize=True, verbose=False):
    ranks = [0 for i in range(len(objs))]
    baselen = len(objs)
    curr_rank = 0
    remain = baselen
    while remain > 0:
        if verbose:
            print('\rRemaining: {0}/{1}        '.format(remain-1, baselen), end='')
            sys.stdout.flush()
        curr_rank += 1
        for i in range(len(objs)):
            if ranks[i] > 0:
                continue
            if not is_dominated(objs, i, ranks, curr_rank, minimize):
                ranks[i] = curr_rank
                remain -= 1
    if verbose:
        print()
    return ranks

def is_dominated2(objs, obj, minimize=True, getall=False): # pop stores the objs 
    """Check if obj is dominated by any one in objs"""
    def is_better(v1, v2, minimize = True):
        """v1 dominiates (is better) v2 if v1 < v2 for minimizing"""
        if minimize:
            return v1 < v2
        else:
            return v1 > v2
    dominating_sols = []
    ov1 = obj
    for i in range(len(objs)):
        ov2 = objs[i]
        k1, k2, k3 = 0, 0, 0
        for j in range(len(objs[0])):
            if is_better(ov1[j], ov2[j], minimize): # ov1[j] < ov2[j]:
                k1 += 1
            elif ov1[j] == ov2[j]:
                k2 += 1
            else:
                k3 += 1
        if k1==0 and k3>0:
            if getall:
                dominating_sols.append(ov2)
            else:
                return True, ov2
    if len(dominating_sols):
        return True, dominating_sols
    return False, dominating_sols


# This is a full version of determining domination status for obj1 and obj2.
#
# Return values:
#   1  obj1 is dominated by obj2    (dominated)
#   0  obj1 = obj2                  (equal)
#  -1  obj1 dominates obj2          (strong dominate)
#  -2  obj1 is not dominated        (not dominated)
#
def domination(objs1, objs2, is_min = True):
    n_better, n_equal, n_worse = 0
    for j in range(len(objs1)):
        if objs1[j] < objs2[j]:
            n_better += 1
        elif objs1[j] == objs2[j]:
            n_equal += 1
        else:
            n_worse += 1
    if n_better==0 and n_worse==0:
        return 1
    if n_equal == len(objs1):
        return 0
    if n_better > 0 and n_worse != 0:
        return -1
    return -2

#
# return true is pop[ix] is dominated by at least one individual in pop, using curr_rank
# pop contains the objective function values for each indivial. [ [obj1, obj2, ...], ... ]
# ranks contains the current ranks for each individual, [ rank, rank, ...], initial -1
#
def is_dominated_old(pop, ix, ranks, curr_rank): # pop stores the objs 
    ov1 = pop[ix]
    for i in range(len(pop)):
        if i==ix:
            continue
        a_rank = ranks[i]
        if a_rank and a_rank<curr_rank:
            continue
        ov2 = pop[i]
        k1, k2, k3 = 0, 0, 0
        for j in range(len(pop[0])):
            if ov1[j] < ov2[j]:
                k1 += 1
            elif ov1[j] == ov2[j]:
                k2 += 1
            else:
                k3 += 1
        if k1==0 and k3>0:
            return True
    return False

def pareto_ranking_old(objs):
    ranks = [-1 for i in range(len(objs))]
    curr_rank = 0
    remain = len(objs)
    while remain>0:
        curr_rank += 1
        for i in range(len(objs)):
            if ranks[i] > 0:
                continue
            if not is_dominated(objs, i, ranks, curr_rank):
                ranks[i] = curr_rank
                remain -= 1
    return ranks
