import re
from model import OptimalityCriteria, solve_SRI
from feasibility_checker import cost, check_feasibility, profile, read_instance
import sys

def parse_answers(file_name, blocking=False):
    answers = []
    with open(file_name) as f:
        for line in f.readlines():
            if line.startswith("roommate") and not blocking:
                current_answer = parse_solution(line)
            elif line.startswith("roommate") and blocking:
                current_answer = [parse_solution(line), []]
            elif line.startswith("UNSATISFIABLE"):
                answers.append(None)
            elif line.startswith("OPTIMUM FOUND"):
                answers.append(current_answer)
                current_answer = None
            elif line.startswith("blocking") and blocking:
                current_answer[1] = parse_solution(line)
    return answers

def parse_solution(line):
    pairs = set()
    for pair_str in line.split():
        match = re.search(r"\d*,\d*", pair_str)
        if match == None:
            raise(ValueError(pair_str))
        match = match.group(0).split(",")
        x, y = int(match[0]), int(match[1])
        if x < y:
            pairs.add((x,y))
    return pairs

def check_optimality_and_feasibility(size, density, criteria):
    if criteria == OptimalityCriteria.EGALITARIAN:
        folder = "egal"
    elif criteria in [OptimalityCriteria.FIRST_CHOICE_MAXIMAL, OptimalityCriteria.RANK_MAXIMAL]:
        folder = "rankmax"
    elif criteria == OptimalityCriteria.ALMOST_STABLE:
        folder = "almost"
    else:
        raise(ValueError("Unsupported criteria", criteria))
    file = "C:\\Users\\Sofia\\Documents\\level5project\\SRI_IP\\data\\outputs\\ASP\\%s-SRI\\output-%s-time-%d-%d.txt" % (folder, folder, size,density)
    try:
        answers = parse_answers(file)
    except FileNotFoundError:
        file = "C:\\Users\\Sofia\\Documents\\level5project\\SRI_IP\\data\\outputs\\ASP\\%s-SRI\\output-%s-%d-%d.txt" % (folder, folder, size,density)
        answers = parse_answers(file)
    file_base = "C:\\Users\\Sofia\\Documents\\level5project\\SRI_IP\\data\\instances\\%d\\i-%d-%d-%d.txt"
    messages = ""
    for i in range(1, len(answers) + 1):
        file = file_base % (size, size, density, i)
        sol = solve_SRI(file, criteria)
        preferences = read_instance(file, 0)
        if sol != answers[i-1]:
            messages += str(i) + " is different\n"
            if criteria != OptimalityCriteria.ALMOST_STABLE or answers[i-1] is None or sol is None:
                messages += "Should be\n"
                messages += str(answers[i-1]) + "\n"
                messages += "We got\n" + str(sol) + "\n"
            if not (answers[i - 1] is None or sol is None):
                messages += "Only in answer: " + str(answers[i-1] - sol) + "\n"
                messages += "Only in solution: " + str(sol - answers[i-1]) + "\n"
            if criteria == OptimalityCriteria.EGALITARIAN:
                messages += compare_egalitarian(sol, answers[i-1], preferences)
            if criteria == OptimalityCriteria.FIRST_CHOICE_MAXIMAL:
                messages += compare_first_choice_maximal(sol, answers[i-1], preferences)
            if criteria == OptimalityCriteria.RANK_MAXIMAL:
                messages += compare_rank_maximal(sol, answers[i-1], preferences)
        if sol is not None:
            feasibility = check_feasibility(preferences, sol) 
            if feasibility is not None:
                messages += "IP " + " : " + str(feasibility) + "\n"
        if answers[i-1] is not None:
            feasibility = check_feasibility(preferences, sol) 
            if feasibility is not None:
                messages += "ASP : " + str(feasibility) + "\n"
    return messages

def compare_egalitarian(sol, answer, preferences):
    messages = ""
    if sol is not None and answer is not None:
        messages += "The cost of ASP: %d\n" % (cost(preferences, answer))
        messages += "The cost of IP: %d\n" % (cost(preferences, sol))
    return messages

def compare_first_choice_maximal(sol, answer, preferences):
    messages = ""
    if sol is not None and answer is not None:
        messages += "The first choices of ASP: %d\n" % (profile(preferences, answer)[0])
        messages += "The first choices of IP: %d\n" % (profile(preferences, sol)[0])
    return messages

def compare_rank_maximal(sol, answer, preferences):
    messages = ""
    if sol is not None and answer is not None:
        messages += "The profile of ASP: %d\n" % (profile(preferences, answer))
        messages += "The profile of IP: %d\n" % (profile(preferences, sol))
    return messages

if __name__ == "__main__":
    messages = []
    criteria_dict = {"rankmax": OptimalityCriteria.RANK_MAXIMAL,
        "1stmax": OptimalityCriteria.FIRST_CHOICE_MAXIMAL,
        "egal": OptimalityCriteria.EGALITARIAN,
        "generous": OptimalityCriteria.EGALITARIAN,
        "almost":OptimalityCriteria.ALMOST_STABLE}
    criteria = criteria_dict[sys.argv[1].lower().strip()]
    sizes = [20,40,60,80,100,150,200]
    if len(sys.argv) <= 2:
        minsize = 20
        maxsize = 100
    elif len(sys.argv) <= 3:
        minsize = int(sys.argv[2])
        maxsize = minsize
    else:
        minsize = int(sys.argv[2])
        maxsize = int(sys.argv[3])
    sizes = [i for i in sizes if i >= minsize and i<= maxsize]
    for density in [25,50,75,100]:
        for size in sizes:
            if not (criteria == OptimalityCriteria.FIRST_CHOICE_MAXIMAL and density == 25 and size == 80):
                messages.append((size, density,
                    check_optimality_and_feasibility(size, density, criteria)))
    for size, density, message in messages:
        print(size, density)
        print(message)
        print()