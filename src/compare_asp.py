import re

def parse_answers(file_name):
    answers = []
    with open(file_name) as f:
        for line in f.readlines():
            if line.startswith("roommate"):
                answers.append(parse_solution(line))
            elif line.startswith("UNSATISFIABLE"):
                answers.append(None)
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
    file = r"C:\Users\Sofia\Documents\level5project\SRI_IP\data\outputs\ASP\egal-SRI\output-egal-time-20-25.txt"
    answers = parse_answers(file)
    for i, a in enumerate(answers):
        print(str(i +1) + " " + str(a))