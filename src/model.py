from gurobipy import *

from utils import *

from enum import Enum

class OptimalityCriteria(Enum):
    NONE = 0
    EGALITARIAN = 1
    FIRST_CHOICE_MAXIMAL = 2

def solve_SRI(preferences, optimisation=OptimalityCriteria.NONE):
    h = PreferenceHelper(preferences)
    m = Model("SRI")

    n = len(preferences)
    # Create the initial matching matrix
    x = m.addVars(n, n, vtype=GRB.BINARY)

    # \sum_{u \in N(v)} x_{u, v} <= 1 for each  v \in V
    m.addConstrs(x.sum([u for u in h.get_neighbours(v)], v) <= 1 for v in range(n))

    # x_{u, v} = 0 for each {u, v} \notin E
    m.addConstrs(x.sum(u, v) == 0 for u,v in h.get_non_edges())

    #\sum_{i \in \{ N(u): i >_u v\}} x_{u, i} +
        #\sum_{j \in { N(v): i >_v u}} x_{v, j} +
        # x_{u, v} <= 1 for each {u, v} \in E
    m.addConstrs(x.sum(u, [i for i in h.get_preferred_neighbours(u, v)])
            + x.sum([i for i in h.get_preferred_neighbours(v, u)], v) 
            + x[u, v] >= 1 for u,v in h.get_edges())

    # x_{u, v} = 0 for each {u, v} \notin E
    m.addConstrs(x[u,v] == x[v,u] for u in range(n) for v in range(n))
    if optimisation == OptimalityCriteria.EGALITARIAN:
        # \sum_{u, v \in V} rank(u, v)x_{u,v}
        m.setObjective(x.prod(h.ranks))
    elif optimisation == OptimalityCriteria.FIRST_CHOICE_MAXIMAL:
        # \sum_{u, v \in V} \delta^1(u,v)x_{u,v}
        m.setObjective(x.prod(h.delta(1)), GRB.MAXIMIZE)
    elif optimisation != OptimalityCriteria.NONE:
        raise(ValueError("Unsupported criteria", optimisation))

    m.optimize()
    n = len(preferences)
    matches = []
    for u in range(n):
        result = ""
        for v in range(n):
            if x[u,v].x > 0:
                result += " x"
                if u < v:
                    matches.append((u + 1,v + 1))
            else:
                result += "  "
        print(result)
    print(matches)


