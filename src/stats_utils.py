import re
import sys
from os import path

def mean(x):
    return sum(x) / len(x)

def collect_stats_ip(filename):
    presolves = []
    solvetimes = []
    with open(filename) as f:
        for line in f.readlines():
            if line.startswith("Gurobi Optimizer version"):
                presolve = 0
                solvetime = 0
            elif line.startswith("Presolve time"):
                match = re.search(r"\d+\.\d+", line)
                if match == None:
                    raise ValueError(line, " is weird")
                presolve = float(match.group(0))
            elif line.startswith("Explored "):
                match = re.search(r"\d+\.\d+", line)
                if match == None:
                    raise ValueError(line, " is weird")
                solvetime = float(match.group(0))
            elif line.strip() == "Solution" or line.strip() == "Solution: None":
                presolves.append(presolve)
                solvetimes.append(solvetime)
    if len(presolves) + len(solvetimes) != 40 or len(presolves) != len(solvetimes):
        print("Warning " + filename + " has invalid number of items")
    return mean(presolves), mean(solvetimes)

def collect_stats_cp(filename):
    presolves = []
    solvetimes = []
    with open(filename) as f:
        for line in f.readlines():
            if line.startswith("solutions"):
                match = re.search(r"modelTime: \d+", line)
                if match == None:
                    raise ValueError(line, " is weird")
                presolves.append(float(match.group(0)[len("modelTime: "):]))
                match = re.search(r"solveTime: \d+", line)
                if match == None:
                    raise ValueError(line, " is weird")
                solvetimes.append(float(match.group(0)[len("solveTime: "):]))
    return mean(presolves)/1000, mean(solvetimes)/1000

if __name__ == "__main__":
    data_folder = sys.argv[1]
    for criteria in ["egal", "1stmax", "almost"]:
        print(criteria)
        for size in [20, 40, 60, 80, 100, 150, 200]:
            for density in [25, 50, 75, 100]:
                print("size: %d, density: %d" % (size, density))
                for solver in ["IP", "CP_new"]:
                    file_path = path.join(data_folder, "outputs", solver,
                        criteria + "-SRI", "output-%s-%d-%d.txt" % (criteria, size, density))
                    try:
                        if solver == "IP":
                            print(solver + ": " + str(collect_stats_ip(file_path)))
                        else:
                            print(solver + ": " + str(collect_stats_cp(file_path)))
                    except FileNotFoundError:
                        print("output-%s-%d-%d.txt does not exist" % (criteria, size, density))