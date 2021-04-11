import re
from model import OptimalityCriteria, solve_SRI
from feasibility_checker import cost, check_feasibility, profile, read_instance
import sys
from os import path

def parse_answers_asp(file_name):
    answers = []
    with open(file_name) as f:
        for line in f.readlines():
            if line.startswith("roommate"):
                current_answer = parse_solution(line)
            elif line.startswith("UNSATISFIABLE"):
                answers.append(None)
            elif line.startswith("OPTIMUM FOUND"):
                answers.append(current_answer)
                current_answer = None
    return answers

def parse_answers(file_name, splitter):
    answers = []
    with open(file_name) as f:
        sol_line = False
        for line in f.readlines():
            if sol_line:
                if line.startswith("solutions: 0") or line.startswith("Solution: None"):
                    answers.append(None)
                else:
                    answers.append(parse_solution_line(line, splitter))
            if line.startswith("Search ended"):
                sol_line = True
            else:
                sol_line = False
    return answers



def parse_solution_line(line, splitter):
    string_pairs = [pair for pair in line.split(splitter)]
    pairs = set()
    for pair in string_pairs:
        if pair.strip() == "":
            continue
        pair = pair.replace("(", "").replace(")", "").split(",")
        pair = (int(pair[0]), int(pair[1]))
        if pair[0] != pair[1]:
            pairs.add(pair)
    return pairs

def parse_solution(line):
    pairs = set()
    for pair_str in line.split():
        match = re.search(r"roommate\(\d*,\d*", pair_str)
        if match == None:
            continue
        match = match.group(0)[len("roommate("):].split(",")
        x, y = int(match[0]), int(match[1])
        if x < y:
            pairs.add((x,y))
    return pairs

def parse_answers_from_parameters(size, density, criteria, solver, file_folder):
    if criteria == OptimalityCriteria.EGALITARIAN:
        folder = "egal"
    elif criteria == OptimalityCriteria.FIRST_CHOICE_MAXIMAL and solver != "ASP":
        folder = "1stmax"
    elif criteria in [OptimalityCriteria.FIRST_CHOICE_MAXIMAL, OptimalityCriteria.RANK_MAXIMAL]:
        folder = "rankmax"
    elif criteria == OptimalityCriteria.ALMOST_STABLE:
        folder = "almost"
    elif criteria == OptimalityCriteria.GENEROUS:
        folder = "generous"
    else:
        raise(ValueError("Unsupported criteria", criteria))
    if solver == "CP":
        solver = "CP_new"
    file = path.join(file_folder, solver, folder + "-SRI", "output-%s-%d-%d.txt" % (folder, size,density))
    if not path.exists(file):
        print(file + " does not exist")
        file = path.join(file_folder, solver, folder + "-SRI", "output-%s-time-%d-%d.txt" % (folder, size,density))
    if solver =="CP_new":
        answers = parse_answers(file, " ")
    elif solver == "IP":
        answers = parse_answers(file, "),(")
    else:
        answers = parse_answers_asp(file)
    return answers


def check_optimality_and_feasibility(size, density, criteria, solver, file_folder):
    answers = parse_answers_from_parameters(size, density, criteria, solver, file_folder)
    messages = ""
    # almost 40-50 is missing the first answer
    if criteria == OptimalityCriteria.ALMOST_STABLE and density == 50 and size == 40 and not cp:
        answers = [None] + answers
    solutions = parse_answers_from_parameters(size, density, criteria, "IP", file_folder)
    for i in range(1, len(answers) + 1):
        preferences = read_instance(size, density, i, 0)
        solution = solutions[i-1]
        answer = answers[i-1]
        if solution != answer:
            messages += str(i) + " is different\n"
            if criteria != OptimalityCriteria.ALMOST_STABLE or answer is None or solution is None:
                messages += "Should be\n"
                messages += str(answer) + "\n"
                messages += "We got\n" + str(solution) + "\n"
            if not (answer is None or solution is None):
                messages += "Only in answer: " + str(answer - solution) + "\n"
                messages += "Only in solution: " + str(solution - answer) + "\n"
            if criteria == OptimalityCriteria.EGALITARIAN:
                messages += compare_egalitarian(solution, answer, preferences)
            if criteria == OptimalityCriteria.FIRST_CHOICE_MAXIMAL:
                messages += compare_first_choice_maximal(solution, answer, preferences)
            if criteria == OptimalityCriteria.RANK_MAXIMAL or criteria == OptimalityCriteria.GENEROUS:
                messages += compare_rank_maximal(solution, answer, preferences)
        if solution is not None:
            feasibility = check_feasibility(preferences, solution) 
            if feasibility is not None:
                messages += "IP " + " : " + str(feasibility) + "\n"
        if answers[i-1] is not None:
            feasibility = check_feasibility(preferences, answer) 
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
        messages += "The profile of ASP: %r\n" % str(profile(preferences, answer))
        messages += "The profile of IP: %r\n" % str(profile(preferences, sol))
    return messages

if __name__ == "__main__":
    messages = []
    criteria_dict = {"rankmax": OptimalityCriteria.RANK_MAXIMAL,
        "1stmax": OptimalityCriteria.FIRST_CHOICE_MAXIMAL,
        "egal": OptimalityCriteria.EGALITARIAN,
        "generous": OptimalityCriteria.GENEROUS,
        "almost":OptimalityCriteria.ALMOST_STABLE}
    criteria = criteria_dict[sys.argv[2].lower().strip()]
    if sys.argv[1] == "default":
        folder = "C:\\Users\\Sofia\\Documents\\level5project\\SRI_IP\\data\\outputs"
    else:
        folder = sys.argv[1]
    sizes = [20, 40, 60, 80, 100, 150, 200]
    solver = sys.argv[3].upper()
    if len(sys.argv) <= 2:
        minsize = 20
        maxsize = 100
    elif len(sys.argv) <= 3:
        minsize = int(sys.argv[4])
        maxsize = minsize
    else:
        minsize = int(sys.argv[4])
        maxsize = int(sys.argv[5])
    sizes = [i for i in sizes if i >= minsize and i<= maxsize]
    for size in sizes :
        for density in [25, 50, 75, 100]:
            # Known non-existing results
            if not ((criteria in [OptimalityCriteria.FIRST_CHOICE_MAXIMAL,
                        OptimalityCriteria.RANK_MAXIMAL] and density == 25 and size == 80)
                    or (criteria == OptimalityCriteria.ALMOST_STABLE and density > 50 and size == 100)):
                messages.append((size, density,
                    check_optimality_and_feasibility(size, density, criteria, solver, folder)))
    for size, density, message in messages:
        print(size, density)
        print(message)
        print()