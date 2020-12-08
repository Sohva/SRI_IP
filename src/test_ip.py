from utils import read_instance
from compare_asp import parse_answers
from feasibility_checker import get_blocking_pairs

def test_verifier():
    preferences = read_instance(60, 25, 5, 0)
    file = "C:\\Users\\Sofia\\Documents\\level5project\\SRI_IP\\data\\outputs\\ASP\\almost-SRI\\output-almost-60-25.txt"
    solution = parse_answers(file)[4]
    blocking_pairs = get_blocking_pairs(preferences, solution)
    assert set(blocking_pairs) == set([(41, 23), (23,  41)])