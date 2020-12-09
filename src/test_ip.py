from utils import read_instance
from compare_asp import parse_answers
from feasibility_checker import get_blocking_pairs, can_get_better_than_current_partner
import re

def parse_blocking_pairs(size, density, duplicates=False):
    file = "C:\\Users\\Sofia\\Documents\\level5project\\SRI_IP\\data\\outputs\\ASP\\almost-SRI\\output-almost-%d-%d.txt" % (size,density)
    answers = []
    with open(file) as f:
        for line in f.readlines():
            if line.startswith("roommate") or line.startswith("blocking"):
                current_answer = parse_solution(line, all)
            elif line.startswith("UNSATISFIABLE"):
                answers.append(None)
            elif line.startswith("OPTIMUM FOUND"):
                answers.append(current_answer)
                current_answer = None
    return answers

def parse_solution(line, duplicates):
    pairs = set()
    for pair_str in line.split():
        match = re.search(r"blocking\(\d*,\d*", pair_str)
        if match == None:
            continue
        match = match.group(0)[len("blocking("):].split(",")
        x, y = int(match[0]), int(match[1])
        if x < y or duplicates:
            pairs.add((x,y))
    return pairs

def test_verifier():
    preferences = read_instance(60, 25, 5, 0)
    file = "C:\\Users\\Sofia\\Documents\\level5project\\SRI_IP\\data\\outputs\\ASP\\almost-SRI\\output-almost-60-25.txt"
    solution = parse_answers(file)[4]
    blocking_pairs = get_blocking_pairs(preferences, solution)
    assert set(blocking_pairs) == set([(41, 23), (23,  41)])

def test_verifier():
    preferences = read_instance(40, 50, 2, 0)
    file = "C:\\Users\\Sofia\\Documents\\level5project\\SRI_IP\\data\\outputs\\ASP\\almost-SRI\\output-almost-40-50.txt"
    solution = parse_answers(file)[0]
    blocking_pairs = get_blocking_pairs(preferences, solution)
    assert set(blocking_pairs) == set()

def get_partners(solution):
    partners = {}
    for pair in solution:
        partners[pair[0]] = pair[1]
        partners[pair[1]] = pair[0]
    return partners

def test_can_get_better_than_1():
    preferences = read_instance(60, 25, 5, 0)
    file = "C:\\Users\\Sofia\\Documents\\level5project\\SRI_IP\\data\\outputs\\ASP\\almost-SRI\\output-almost-60-25.txt"
    solution = parse_answers(file)[4]
    better_options = can_get_better_than_current_partner(preferences, get_partners(solution), 41)
    assert set(better_options) == set([23])

def test_can_get_better_than_simple1():
    preferences = [[2,3,4], [3,1,4], [1,2,4], [3, 2, 1]]
    solution = [[1,2], [3,4]]
    better_options = can_get_better_than_current_partner(preferences, get_partners(solution), 2)
    assert set(better_options) == set([3])

def test_can_get_better_than_simple2():
    preferences = [[2,3,4], [3,1,4], [1,2,4], [3, 2, 1]]
    solution = [[1,2], [3,4]]
    better_options = can_get_better_than_current_partner(preferences, get_partners(solution), 3)
    assert set(better_options) == set([2])

def test_can_get_better_than_simple3():
    preferences = [[2,3,4], [3,1,4], [1,2,4], [3, 2, 1]]
    solution = [[1,2], [3,4]]
    better_options = can_get_better_than_current_partner(preferences, get_partners(solution), 1)
    assert set(better_options) == set()

def test_parse_almost_solution():
    file = "C:\\Users\\Sofia\\Documents\\level5project\\SRI_IP\\data\\outputs\\ASP\\almost-SRI\\output-almost-40-75.txt"
    solution = parse_answers(file)[0]
    assert solution == set([(10,28), (38,40), (32,37),
                            (3,34), (33,39), (27,31),
                            (21,26), (7,24), (11,22),
                            (5,19), (17,29), (13,16),
                            (12,36), (1,35), (6,30),
                            (20,25), (18,23), (9,15),
                            (4,14), (2,8)])