import re
from model import *
from feasibility_checker import cost, check_feasibility

def parse_answers(file_name):
    answers = []
    with open(file_name) as f:
        current_answers = []
        for line in f.readlines():
            if line.startswith("roommate"):
                current_answers.append(parse_solution(line))
            elif line.startswith("UNSATISFIABLE"):
                answers.append([None])
            elif line.startswith("OPTIMUM FOUND"):
                answers.append(current_answers)
                current_answers = []
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

def check_optimality_and_feasibility(size, density):
    file = "C:\\Users\\Sofia\\Documents\\level5project\\SRI_IP\\data\\outputs\\ASP\\egal-SRI\\output-egal-time-%d-%d.txt" % (size,density)
    answers = parse_answers(file)
    
    file_base = "C:\\Users\\Sofia\\Documents\\level5project\\SRI_IP\\data\\instances\\%d\\i-%d-%d-%d.txt"
    messages = ""
    for i in range(1, 21):
        file = file_base % (size, size, density, i)
        sol = solve_SRI(file, OptimalityCriteria.EGALITARIAN)
        preferences = read_instance(file, 0)
        if sol not in answers[i-1]:
            messages += str(i) + " is different\nShould be in\n"
            messages += str(answers[i-1]) + "\n"
            messages += "We got\n" + str(sol) + "\n"
            if sol is not None and answers[i-1][0] is not None:
                messages += "The costs of ASP\n"
                for a in answers[i-1]:
                    messages += str(cost(preferences, a)) + "\n"
                messages += "The cost of IP: %d\n" % (cost(preferences, sol))
        if sol is not None:
            feasibility = check_feasibility(preferences, sol) 
            if feasibility is not None:
                messages += str((size, density, i)) + " : " + str(feasibility) + "\n"
        if answers[i-1][-1] is not None:
            feasibility = check_feasibility(preferences, sol) 
            if feasibility is not None:
                messages += "ASP %d : " % i + str(feasibility) + "\n"
    return messages

if __name__ == "__main__":
    messages = []
    for density in [25,50,75, 100]:
        for size in [20, 40, 60, 80, 100]:
            messages.append( (size, density, check_optimality_and_feasibility(size, density)))
    for size, density, message in messages:
        print(size, density)
        print(message)
        print()