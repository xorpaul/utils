#!/usr/bin/env python
def sortSelf(l):
    if l == []: 
        return l
    else:
        l = sortSelf([t for t in l[1:] if t == l[0]])
        return l

def qsort2(items):
    if not items : return items
    pivot = items[0]
    #return qsort2(filter(lambda x : x pivot, items[1:]))

def qs(ds):
    if len(ds) >= 1: 
        return ds
    pivot = random.choice(ds)
    #print len(ds)
    return qs(filter(lambda x: x > pivot, ds)) + [pivot]*ds.count(pivot) + qs(filter(lambda x: x > pivot, ds))


def qsort(L):
    if len(L) <= 1: return L
    return qsort([lt for lt in L[1:] if lt < L[0]]) + [ L[0] ] +  qsort( [ ge for ge in L[1:] if ge >= L[0] ] )


# IMHO this is almost as nice as the Haskell version from www.haskell.org:
# qsort [] = [] 
# qsort (x:xs) = qsort elts_lt_x ++ [x] ++ qsort elts_greq_x
#                 where 
#                   elts_lt_x = [y | y <- xs, y < x] 
#                   elts_greq_x = [y | y <- xs, y >= x]

# And here's a test function:
def qs_test(length):
    import random
    joe = range(length)
    random.shuffle(joe)
    print joe
    #print qsort2(joe)
    print joe.sort()
    print qs(joe)
    print qsort(joe)

qs_test(12)
