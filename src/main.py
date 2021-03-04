
from model import solve_SRI, OptimalityCriteria
from utils import read_instance
from feasibility_checker import check_feasibility

preferences = [[8, 2, 9, 3, 6, 4, 5, 7, 10], [4, 3, 8, 9, 5, 1, 10, 6, 7], [5, 6, 8, 2, 1, 7, 10, 4, 9], [10, 7, 9, 3, 1, 6, 2, 5, 8], [7, 4, 10, 8, 2, 6, 3, 1, 9], [2, 8, 7, 3, 4, 10, 1, 5, 9], [2, 1, 8, 3, 5, 10, 4, 6, 9], [10, 4, 2, 5, 6, 7, 1, 3, 9], [6, 7, 2, 5, 10, 3, 4, 8, 1], [3, 1, 6, 5, 2, 9, 8, 4, 7]]
preferences = [[2, 3, 4], [3, 1, 4], [1,2, 4], [1]]
preferences = [[u - 1 for u in ls] for ls in preferences]

for size in [20]:
    for density in range(25, 26):
        for i in range(1,21):
            print(size, density, i)
            print(solve_SRI(size, density, i, OptimalityCriteria.EGALITARIAN))

