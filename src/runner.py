from os import mkdir
from model import OptimalityCriteria, solve_SRI
import sys

if __name__ == "__main__":
    criteria_dict = {"rankmax": OptimalityCriteria.RANK_MAXIMAL,
        "1stmax": OptimalityCriteria.FIRST_CHOICE_MAXIMAL,
        "egal": OptimalityCriteria.EGALITARIAN,
        "generous": OptimalityCriteria.EGALITARIAN,
        "almost":OptimalityCriteria.ALMOST_STABLE}
    criteria_string = sys.argv[1].lower().strip()
    criteria = criteria_dict[criteria_string]
    base = "C:\\Users\\Sofia\\Documents\\level5project\\SRI_IP\\data\\"
    out = "outputs\\IP";
    folder = base + out + "\\" + criteria_string  + "-SRI\\";
    try:
        mkdir(folder)
    except FileExistsError:
        pass
    for size in [150, 200]:
        for density in range(25, 101, 25):
            filename = folder + "output" + "-" + criteria_string + "-" + str(size) + "-" + str(density) + ".txt"
            with open(filename, "w") as f:
                for i in range(1,21):
                    f.write("Instance\n")
                    sol = solve_SRI(size, density, i, criteria)
                    if not sol:
                        f.write("solutions: 0\n\n")
                    else:
                        f.write(str(solve_SRI(size, density, i, criteria))[1:-1])
                        f.write("\n\n")
