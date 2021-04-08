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

def collect_stats_ip(filename, full=True):
    if full:
        words = ["readtimes", "buildtimes", "presolvetimes", "solvetimes", "totaltimes"]
    else:
        words = ["totaltimes"]
    all_stats = _init_stats(*words)
    with open(filename) as f:
        for line in f.readlines():
            if full:
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
                elif line.startswith("Readtime: "):
                    readtime = _get_time("Readtime", line)/ 1e9
                elif line.startswith("Buildtime: "):
                    buildtime = _get_time("Buildtime", line) / 1e9
            if line.startswith("Totaltime: "):
                totaltime = _get_time("Totaltime", line) / 1e9
            elif line.startswith("(") or line.strip() == "Solution: None":
                    if line.strip() == "Solution: None":
                        stats = all_stats[False]
                    else:
                        stats = all_stats[True]
                    if full:
                        stats["presolvetimes"].append(presolve)
                        stats["solvetimes"].append(solvetime)
                        stats["readtimes"].append(readtime)
                        stats["buildtimes"].append(buildtime)
                    stats["totaltimes"].append(totaltime)

    return all_stats

def _get_time(attribute, line):
    match = re.search(attribute + ": \d+", line)
    if match == None:
        raise ValueError(line, " is weird")
    return float(match.group(0)[len(attribute) + 2:])

def collect_stats_cp(filename, full=True):
    if full:
        all_stats = ["readtimes", "buildtimes", "solvetimes", "totaltimes"]
    else:
        all_stats = ["totaltimes"]
    all_stats = _init_stats(*all_stats)
    with open(filename) as f:
        for line in f.readlines():
            if line.startswith("solutions"):
                if line.startswith("solutions: 0"):
                    stats = all_stats[False]
                else:
                    stats = all_stats[True]
                if full:
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
    for criteria in ["egal", "almost", "rankmax", "generous", "1stmax"]:
        print(criteria)
        for size in [20,40,60, 80, 100, 150, 200]:
            for density in [25, 50, 75, 100]:
                print("size: %d, density: %d" % (size, density))
                for solver in ["IP", "CP_new"]:
                    file_path = path.join(data_folder, solver,
                        criteria + "-SRI", "output-%s-%d-%d.txt" % (criteria, size, density))
                    try:
                        full = criteria not in ["rankmax", "generous"]
                        if solver == "IP":
                            stats = collect_stats_ip(file_path, full)
                        else:
                            stats = collect_stats_cp(file_path, full)
                        print(solver + "\n" + stats_str(stats))
                    except FileNotFoundError:
                        print("%s does not exist" % file_path)
                    except ValueError as e:
                        print("%s has invalid line %r"  % (file_path, e))