from os import mkdir
from os import path
from model import OptimalityCriteria, solve_SRI
from contextlib import redirect_stdout
import sys

def get_file_name(data_folder, size, density, i):
    return path.join(data_folder, "instances", str(size), "i-%d-%d-%d.txt" % (size, density, i))

if __name__ == "__main__":
    criteria_dict = {"rankmax": OptimalityCriteria.RANK_MAXIMAL,
        "1stmax": OptimalityCriteria.FIRST_CHOICE_MAXIMAL,
        "egal": OptimalityCriteria.EGALITARIAN,
        "generous": OptimalityCriteria.GENEROUS,
        "almost":OptimalityCriteria.ALMOST_STABLE,
        "none":OptimalityCriteria.NONE}
    criteria_string = sys.argv[2].lower().strip()
    criteria = criteria_dict[criteria_string]
    if sys.argv[1] == "default":
        base = "C:\\Users\\Sofia\\Documents\\level5project\\SRI_IP\\data\\"
    else:
        base = sys.argv[1]
    out = path.join(base, "outputs", "IP")
    folders = [base, "outputs", "IP", criteria_string +"-SRI"]
    folder = path.join(*folders)
    for i in range(1, len(folders)+1):
        try:
            mkdir(path.join(*folders[0:i]))
        except FileExistsError:
            pass
    sizes = [20, 40, 60, 80, 100, 150, 200]
    if len(sys.argv) <= 3:
        minsize = 20
        maxsize = 100
    else:
        minsize = int(sys.argv[3])
        maxsize = int(sys.argv[4])
    sizes = [i for i in sizes if i >= minsize and i<= maxsize]
    densities = range(25, 101, 25)
    if len(sys.argv) > 5:
        densities = [int(sys.argv[5])]
    instances = range(1,21)
    if len(sys.argv) > 6:
        instances = [int(sys.argv[6])]
    for size in sizes:
        for density in densities:
            filename = path.join(folder,"output" + "-" + criteria_string + "-" + str(size) + "-" + str(density) + ".txt")
            with open(filename, 'w+') as f:
                with redirect_stdout(f):
                    for i in instances:
                        sol = solve_SRI(get_file_name(base, size, density, i), optimisation=criteria)
                        print("Search ended")
                        if not sol:
                            print("Solution: None\n")
                        else:
                            print(str(sol).replace(" ", "")[1:-1])
                            print("\n")
