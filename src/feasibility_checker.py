from utils import *
from model import *

# Takes the preferences and answers indexed from 1
def check_feasibility(preferences, answer):
    # Write pairs into dictionary for easy lookup
    # Check that the pairs find each other acceptable
    for pair in answer:
        if (not pair[0] in preferences[pair[1] - 1]) or (not pair[1] in preferences[pair[0] - 1]):
            return pair, "Not acceptable"
    blocking_pairs = get_blocking_pairs(preferences, answer)
    if blocking_pairs:
        return blocking_pairs, str(len(blocking_pairs)) + " blocking"
    return None

def get_blocking_pairs(preferences, answer):
    partners = {}
    for pair in answer:
        partners[pair[0]] = pair[1]
        partners[pair[1]] = pair[0]
    blocking_pairs = []
    for agent in range(1, len(preferences) + 1):
        for better_option in can_get_better_than_current_partner(
                preferences, partners, agent):
            blocking_pairs.append((agent, better_option))
    return blocking_pairs

def can_get_better_than_current_partner(preferences, partners, j):
    better_options = []
    if j not in partners:
        preferred_agents = preferences[j-1]
    else:
        preferred_agents = preferences[j-1][0:preferences[j-1].index(partners[j])]
    for i in preferred_agents:
        i_prefs = preferences[i - 1]
        # i finds j acceptable
        if (j in i_prefs) and (
                # i is not partnered
                not i in partners
                # i prefers j to their current partner
                or i_prefs.index(j) < i_prefs.index(partners[i])):
            better_options.append(i)
    return better_options

def cost(preferences, answer):
    cost = 0
    for pair in answer:
        cost += preferences[pair[0] - 1].index(pair[1]) + 1
        cost += preferences[pair[1] - 1].index(pair[0]) + 1
    return cost

def profile(preferences, answer):
    profile = [0 for _ in range(len(preferences))]
    for pair in answer:
        profile[preferences[pair[0] - 1].index(pair[1])] += 1
        profile[preferences[pair[1] - 1].index(pair[0])] += 1
    return profile

if __name__ == "__main__":
    size = 20
    density = 75
    file_base = "C:\\Users\\Sofia\\Documents\\level5project\\SRI_IP\\data\\instances\\%d\\i-%d-%d-%d.txt"
    messages = ""
    for i in range(1, 21):
        file = file_base % (size, size, density, i)
        sols = solve_SRI(file, optimisation=OptimalityCriteria.EGALITARIAN)
        preferences = read_instance(file, 0)
        messages += "**** " +str(i) + " ****\n"
        if sols is None:
            messages += "UNFEASIBLE\n"
        else:
            messages += str(check_feasibility(preferences, sols)) + "\n"
    print(messages)