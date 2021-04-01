import re
import sys
from os import path

def mean(x):
    return sum(x) / len(x)

def _init_stats(*args):
    all_stats = {}
    all_stats[True] = {}
    all_stats[False] = {}
    for _, stats in all_stats.items():
        for arg in args:
            stats[arg] = []
    return all_stats

def collect_stats_ip(filename):
    all_stats = _init_stats("readtimes", "buildtimes", "presolvetimes", "solvetimes", "totaltimes")
    with open(filename) as f:
        for line in f.readlines():
            if line.startswith("Gurobi Optimizer version"):
                presolve = 0
                solvetime = 0
            elif line.startswith("Presolve time"):
                match = re.search(r"\d+\.\d+", line)
                if match == None:
                    raise ValueError(line + " is weird")
                presolve = float(match.group(0))
            elif line.startswith("Explored "):
                match = re.search(r"\d+\.\d+", line)
                if match == None:
                    raise ValueError(line, " is weird")
                solvetime = float(match.group(0))
            elif line.startswith("(") or line.strip() == "Solution: None":
                if line.strip() == "Solution: None":
                    stats = all_stats[False]
                else:
                    stats = all_stats[True]
                stats["presolvetimes"].append(presolve)
                stats["solvetimes"].append(solvetime)
                stats["readtimes"].append(readtime)
                stats["totaltimes"].append(totaltime)
                stats["buildtimes"].append(buildtime)
            elif line.startswith("Readtime: "):
                readtime = _get_time("Readtime", line)
            elif line.startswith("Totaltime: "):
                totaltime = _get_time("Totaltime", line)
            elif line.startswith("Buildtime: "):
                buildtime = _get_time("Buildtime", line)
    return all_stats

def _get_time(attribute, line):
    match = re.search(attribute + ": \d+", line)
    if match == None:
        raise ValueError(line, " is weird")
    return float(match.group(0)[len(attribute) + 2:])

def collect_stats_cp(filename):
    all_stats = _init_stats("readtimes", "buildtimes", "solvetimes", "totaltimes")
    with open(filename) as f:
        for line in f.readlines():
            if line.startswith("solutions"):
                if line.startswith("solutions: 0"):
                    stats = all_stats[False]
                else:
                    stats = all_stats[True]
                stats["readtimes"].append(_get_time("readTime", line)/1000)
                stats["buildtimes"].append(_get_time("modelTime", line)/1000)
                stats["solvetimes"].append(_get_time("solveTime", line)/1000)
                stats["totaltimes"].append(_get_time("totalTime", line)/1000)
    return all_stats

def stats_str(stats):
    toprint = ""
    for has_solution, stat in stats.items():
        toprint += "Has solution: " + str(has_solution) + "  "
        for criteria, value in stat.items():
            try:
                me = "%.3f" % mean(value)
            except ZeroDivisionError:
                me = "-"
            toprint += criteria + ": " + me + "  "
        toprint += "\n"
    return toprint

if __name__ == "__main__":
    data_folder = sys.argv[1]
    for criteria in ["egal", "almost"]:
        print(criteria)
        for size in [20,40,60,80,100]:
            for density in [25, 50, 75, 100]:
                print("size: %d, density: %d" % (size, density))
                for solver in ["IP", "CP_new"]:
                    file_path = path.join(data_folder, solver,
                        criteria + "-SRI", "output-%s-%d-%d.txt" % (criteria, size, density))
                    try:
                        if solver == "IP":
                            stats = collect_stats_ip(file_path)
                        else:
                            stats = collect_stats_cp(file_path)
                        print(solver + "\n" + stats_str(stats))
                    except FileNotFoundError:
                        print("output-%s-%d-%d.txt does not exist" % (criteria, size, density))