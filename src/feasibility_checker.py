from utils import *
from model import *

# Takes the preferences and answers indexed from 1
def check_feasibility(preferences, answer):
    # Write pairs into dictionary for easy lookup
    partners = {}
    for pair in answer:
        partners[pair[0]] = pair[1]
        partners[pair[1]] = pair[0]
    # Check that the pairs find each other acceptable
    for pair in answer:
        if (not pair[0] in preferences[pair[1] - 1]) or (not pair[1] in preferences[pair[0] - 1]):
            return pair, "Not acceptable"
        # Check for blocking pairs
        a = can_get_better_than(preferences, partners, *pair)
        if a is not None:
            return pair, "blocked by " + str(a) + "," + str(pair[0])
        a = can_get_better_than(preferences, partners, *reversed(pair))
        if a is not None:
            return pair, "blocked by " + str(a) + "," + str(pair[1])
    # Check unmatched agents
    for i in range(1, len(preferences) + 1):
        if not i in partners:
            a = can_get_better_than(preferences, partners, i)
            if a is not None:
                return pair, "blocked by " + str(a) + "," + str(i)
    return None

def can_get_better_than(preferences, partners, j, i=None):
    if i is None:
        rank = len(preferences)
    else:
        rank = preferences[j-1].index(i)
    for preferred_agent in preferences[j-1][0:rank]:
        prefs = preferences[preferred_agent - 1]
        if prefs.index(j) < prefs.index(partners[preferred_agent]):
            return preferred_agent
    return None

if __name__ == "__main__":
    preferences = [[2,4,3], [3,1,4], [1,2,4], [1,2]]
    answers = [[(1,2), (3,4)], [(1,3), (2,4)], [(1,4), (2,3)]]
    file_start = r"C:\Users\Sofia\Documents\level5project\SRI_IP\data\instances\20\i-20-25-"
    for i in range(1, 21):
        file = file_start + str(i)+ ".txt"
        sols = solve_SRI(file, OptimalityCriteria.EGALITARIAN)
        preferences = read_instance(file, 0)
        print("**** " +str(i) + " ****")
        print(check_feasibility(preferences, sols))