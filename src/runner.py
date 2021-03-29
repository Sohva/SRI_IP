from os import mkdir
from os import path
from model import OptimalityCriteria, solve_SRI
from contextlib import redirect_stdout
import sys

if __name__ == "__main__":
    criteria_dict = {"rankmax": OptimalityCriteria.RANK_MAXIMAL,
        "1stmax": OptimalityCriteria.FIRST_CHOICE_MAXIMAL,
        "egal": OptimalityCriteria.EGALITARIAN,
        "generous": OptimalityCriteria.GENEROUS,
        "almost":OptimalityCriteria.ALMOST_STABLE}
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
    for size in sizes:
        for density in range(25, 101, 25):
            filename = path.join(folder,"output" + "-" + criteria_string + "-" + str(size) + "-" + str(density) + ".txt")
            with open(filename, 'w+') as f:
                with redirect_stdout(f):
                    for i in range(1,21):
                        sol = solve_SRI(size, density, i, criteria)
                        if not sol:
                            print("Solution: None\n")
                        else:
                            print("Solution")
                            print(str(sol).replace(" ", "")[1:-1])
                            print("\n")
