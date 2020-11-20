from gurobipy import *
from itertools import chain
from collections import defaultdict
m = Model("SRI")


preferences = [[8, 2, 9, 3, 6, 4, 5, 7, 10], [4, 3, 8, 9, 5, 1, 10, 6, 7], [5, 6, 8, 2, 1, 7, 10, 4, 9], [10, 7, 9, 3, 1, 6, 2, 5, 8], [7, 4, 10, 8, 2, 6, 3, 1, 9], [2, 8, 7, 3, 4, 10, 1, 5, 9], [2, 1, 8, 3, 5, 10, 4, 6, 9], [10, 4, 2, 5, 6, 7, 1, 3, 9], [6, 7, 2, 5, 10, 3, 4, 8, 1], [3, 1, 6, 5, 2, 9, 8, 4, 7]]
for i, ls in enumerate(preferences):
    preferences[i] = [j - 1 for j in ls]
print(preferences)
n = len(preferences) # number of agents

def get_neighbours(i):
    return preferences[i]

def get_neighbour_pairs():
    for v in range(n):
        for u in get_neighbours(v):
            yield (u, v)

def get_edges():
    for v in range(n):
        for u in get_neighbours(v):
            if u < v:
                yield (u, v)

def get_non_edges():
    for v in range(n):
        for u in range(n):
            if u <= v and u not in get_neighbours(v):
                yield u, v

def get_preferred_neighbours(u, v):
    for i in get_neighbours(u):
        if i != v:
            yield i
        else:
            break

ranks = defaultdict(lambda: 0)
for u, prefs in enumerate(preferences):
    for index, v in enumerate(prefs):
        ranks[(u, v)] = index + 1

assert ranks[9, 8] == 6
assert ranks[3, 4] == 8

# Create the initial matching matrix
x = m.addVars(n, n, vtype=GRB.BINARY)

m.addConstrs(x.sum([u for u in get_neighbours(v)], v) <= 1 for v in range(n))
m.addConstrs(x.sum(u, v) == 0 for u,v in get_non_edges())
m.addConstrs(x.sum(u, [i for i in get_preferred_neighbours(u, v)])
            + x.sum([i for i in get_preferred_neighbours(v, u)], v) 
            + x[u, v] >= 1 for u,v in get_edges())
m.addConstrs(x[u,v] == x[v,u] for u in range(n) for v in range(n))

m.setObjective(x.prod(ranks))

m.optimize()

matches = []
for u in range(n):
    str = ""
    for v in range(n):
        if x[u,v].x > 0:
            str += " x"
            if u < v:
                matches.append((u + 1,v + 1))
        else:
            str += "  "
    print(str)
print(matches)