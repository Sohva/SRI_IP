from gurobipy import *

from utils import read_instance, PreferenceHelper
import time
from enum import Enum

class OptimalityCriteria(Enum):
    NONE = 0
    EGALITARIAN = 1
    FIRST_CHOICE_MAXIMAL = 2
    RANK_MAXIMAL = 3
    GENEROUS = 4
    ALMOST_STABLE = 5

def solve_SRI(preferences, density=None, index=None, optimisation=OptimalityCriteria.NONE):
    start_read_time = time.time_ns()
    start_total_time = start_read_time
    if density is not None:
        if index is not None:
            preferences = read_instance(preferences, density, index)
        else:
            raise(ValueError("Too few arguments", preferences, density, index))
    elif type(preferences) == type(""):
        preferences = read_instance(preferences)
    h = PreferenceHelper(preferences)
    print("Readtime: " + str((time.time_ns() - start_read_time)) + " ns")
    start_build_time = time.time_ns()
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

    has_solution = True

    if optimisation == OptimalityCriteria.EGALITARIAN:
        m.Params.BranchDir = -1
        m.Params.Heuristics = 0
        m.Params.PrePasses = 2
        m.setObjective(x.prod(h.ranks))
    elif optimisation == OptimalityCriteria.FIRST_CHOICE_MAXIMAL:
        m.Params.Heuristics = 0
        m.Params.MIPFocus = 3
        m.Params.NoRelHeurWork = 60
        # \sum_{u, v \in V} \delta^1(u,v)x_{u,v}
        m.setObjective(x.prod(h.delta(1)), GRB.MAXIMIZE)
    elif optimisation == OptimalityCriteria.RANK_MAXIMAL:
        m.Params.ScaleFlag  = 1
        m.Params.Heuristics = 0
        m.Params.BranchDir = 1
        m.params.PrePasses =5
        m.Params.MIPFocus = 3
        for i in range(1, h.max_pref_length - 1):
            delta_i = h.delta(i)
            m.setObjective(x.prod(delta_i), GRB.MAXIMIZE)
            m.optimize()
            if not hasattr(m, "ObjVal"):
                has_solution = False
                break
            m.addConstr(x.prod(delta_i) >= m.ObjVal)
        m.setObjective(x.prod(h.delta(h.max_pref_length - 1)), GRB.MAXIMIZE)
    elif optimisation == OptimalityCriteria.GENEROUS:
        m.Params.DegenMoves = 4
        m.Params.Heuristics = 0
        m.Params.PrePasses = 5
        m.Params.BranchDir = -1
        m.Params.MIPFocus = 2
        for i in range(h.max_pref_length, 1 , -1):
            delta_i = h.delta(i)
            m.setObjective(x.prod(delta_i))
            m.optimize()
            if not hasattr(m, "ObjVal"):
                has_solution = False
                break
            m.addConstr(x.prod(delta_i) <= m.ObjVal)
        m.setObjective(x.prod(h.delta(1)))
    elif optimisation == OptimalityCriteria.ALMOST_STABLE:
        m.Params.NormAdjust = 0
        m.Params.Heuristics = 0.001
        m.Params.VarBranch = 1
        m.Params.GomoryPasses = 15
        m.Params.PreSparsify = 0
        b = m.addVars(n, n, vtype=GRB.BINARY)
        m.addConstrs(x.sum(u, [i for i in h.get_preferred_neighbours(u, v)])
                + x.sum([i for i in h.get_preferred_neighbours(v, u)], v) 
                + x[u, v] + b[u,v] >= 1
                    for u,v in h.get_edges())
        m.setObjective(b.sum())
    elif optimisation != OptimalityCriteria.NONE:
        raise(ValueError("Unsupported criteria", optimisation))
    print("Buildtime: " + str(time.time_ns() - start_build_time) + " ns")
    if has_solution:
        m.optimize()
    print("Totaltime: " + str((time.time_ns() - start_total_time)) + " ns")
    n = len(preferences)
    matches = set()
    if not hasattr(x[0,0], "x"):
        return None
    for u in range(n):
        for v in range(n):
            if x[u,v].x > 0 and u < v:
                matches.add((u + 1,v + 1))
    return matches


