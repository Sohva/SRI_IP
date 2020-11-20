from gurobipy import *
from itertools import chain
m = Model("SRI")


preferences = [
    [1, 2, 3],
    [2, 0, 3],
    [0, 1, 3],
    [2]
]
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


# Create the initial matching matrix
x = m.addVars(n, n, vtype=GRB.BINARY)

m.addConstrs(x.sum([u for u in get_neighbours(v)], v) <= 1 for v in range(n))
m.addConstrs(x.sum(u, v) == 0 for u,v in get_non_edges())
m.addConstrs(x.sum(u, [i for i in get_preferred_neighbours(u, v)])
            + x.sum([i for i in get_preferred_neighbours(v, u)], v) 
            + x[u, v] >= 1 for u,v in get_edges())
m.addConstrs(x[u,v] == x[v,u] for u in range(n) for v in range(n))

m.optimize()

print(m.getVars())
for u in range(n):
    str = ""
    for v in range(n):
        if x[u,v].x > 0:
            str += " x"
        else:
            str += "  "
    print(str)