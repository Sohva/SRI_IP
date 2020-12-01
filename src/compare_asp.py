import re
from model import *

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

if __name__ == "__main__":
    size = 20
    density = 75
    file = "C:\\Users\\Sofia\\Documents\\level5project\\SRI_IP\\data\\outputs\\ASP\\egal-SRI\\output-egal-time-%d-%d.txt" % (size,density)
    answers = parse_answers(file)
    
    file_base = "C:\\Users\\Sofia\\Documents\\level5project\\SRI_IP\\data\\instances\\%d\\i-%d-%d-%d.txt"
    messages = ""
    for i in range(1, 21):
        file = file_base % (size, size, density, i)
        sol = solve_SRI(file, OptimalityCriteria.EGALITARIAN)
        if sol not in answers[i-1]:
            messages += str(i) + " is wrong\n"
            messages += "Should be in\n"
            messages += str(answers[i-1]) + "\n"
            messages += "We got\n"
            messages += str(sol) + "\n"
    print(messages)