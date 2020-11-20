
from model import solve_SRI, OptimalityCriteria

preferences = [[8, 2, 9, 3, 6, 4, 5, 7, 10], [4, 3, 8, 9, 5, 1, 10, 6, 7], [5, 6, 8, 2, 1, 7, 10, 4, 9], [10, 7, 9, 3, 1, 6, 2, 5, 8], [7, 4, 10, 8, 2, 6, 3, 1, 9], [2, 8, 7, 3, 4, 10, 1, 5, 9], [2, 1, 8, 3, 5, 10, 4, 6, 9], [10, 4, 2, 5, 6, 7, 1, 3, 9], [6, 7, 2, 5, 10, 3, 4, 8, 1], [3, 1, 6, 5, 2, 9, 8, 4, 7]]

solve_SRI(preferences, OptimalityCriteria.EGALITARIAN)
