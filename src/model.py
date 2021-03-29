from gurobipy import *

from utils import read_instance, PreferenceHelper

from enum import Enum

class OptimalityCriteria(Enum):
    NONE = 0
    EGALITARIAN = 1
    FIRST_CHOICE_MAXIMAL = 2
    RANK_MAXIMAL = 3
    GENEROUS = 4
    ALMOST_STABLE = 5

def solve_SRI(preferences, density=None, index=None, optimisation=OptimalityCriteria.NONE):
    if density is not None:
        if index is not None:
            preferences = read_instance(preferences, density, index)
        else:
            raise(ValueError("Too few arguments", preferences, density, index))
    elif type(preferences) == type(""):
        preferences = read_instance(preferences)
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
    if not optimisation == OptimalityCriteria.ALMOST_STABLE:
        m.addConstrs(x.sum(u, [i for i in h.get_preferred_neighbours(u, v)])
                + x.sum([i for i in h.get_preferred_neighbours(v, u)], v) 
                + x[u, v] >= 1
                    for u,v in h.get_edges())

    # x_{u, v} = x_{v, u} for each {u, v} \notin E
    m.addConstrs(x[u,v] == x[v,u] for u in range(n) for v in range(n))

    if optimisation == OptimalityCriteria.EGALITARIAN:
        # \sum_{u, v \in V} rank(u, v)x_{u,v}
        m.setObjective(x.prod(h.ranks))
    elif optimisation == OptimalityCriteria.FIRST_CHOICE_MAXIMAL:
        # \sum_{u, v \in V} \delta^1(u,v)x_{u,v}
        m.setObjective(x.prod(h.delta(1)), GRB.MAXIMIZE)
    elif optimisation == OptimalityCriteria.RANK_MAXIMAL:
        for i in range(1, h.max_pref_length - 1):
            delta_i = h.delta(i)
            m.setObjective(x.prod(delta_i), GRB.MAXIMIZE)
            m.optimize()
            if not hasattr(m, "ObjVal"):
                return None
            m.addConstr(x.prod(delta_i) >= m.ObjVal)
        m.setObjective(x.prod(h.delta(h.max_pref_length - 1)), GRB.MAXIMIZE)
    elif optimisation == OptimalityCriteria.GENEROUS:
        for i in range(h.max_pref_length, 1, -1):
            delta_i = h.delta(i)
            m.setObjective(x.prod(delta_i))
            m.optimize()
            if not hasattr(m, "ObjVal"):
                return None
            m.addConstr(x.prod(delta_i) <= m.ObjVal)
        m.setObjective(x.prod(h.delta(1)))
    elif optimisation == OptimalityCriteria.ALMOST_STABLE:
        b = m.addVars(n, n, vtype=GRB.BINARY)
        m.addConstrs(x.sum(u, [i for i in h.get_preferred_neighbours(u, v)])
                + x.sum([i for i in h.get_preferred_neighbours(v, u)], v) 
                + x[u, v] + b[u,v] >= 1
                    for u,v in h.get_edges())
        m.setObjective(b.sum())
    elif optimisation != OptimalityCriteria.NONE:
        raise(ValueError("Unsupported criteria", optimisation))

    m.optimize()
    n = len(preferences)
    matches = set()
    if not hasattr(x[0,0], "x"):
        return None
    for u in range(n):
        for v in range(n):
            if x[u,v].x > 0 and u < v:
                matches.add((u + 1,v + 1))
    return matches


