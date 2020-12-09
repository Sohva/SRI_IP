from compare_asp import parse_answers
from feasibility_checker import check_feasibility
from utils import read_instance
from test_ip import parse_blocking_pairs

def test_feasibility_checker():
    for size in [40, 60, 80]:
        for density in [25, 50, 75, 100]:
            if size == 40 and density == 25:
                continue
            blocking_pairs = parse_blocking_pairs(size, density, True)
            answers = parse_answers("C:\\Users\\Sofia\\Documents\\level5project\\SRI_IP\\data\\outputs\\ASP\\almost-SRI\\output-almost-%d-%d.txt" % (size, density))
            if size == 40 and density == 50:
                answers = [None] + answers
                blocking_pairs = [None] + blocking_pairs
            for i, answer in enumerate(answers):
                # Known non-existing/weird answers
                if (size == 40 and density == 50 and i == 0) or (
                    size == 60 and density == 25 and i == 19):
                    continue
                preferences = read_instance(size, density, i + 1, 0)
                print(size, density, i+1)
                feasibility = check_feasibility(preferences, answer)
                assert (not feasibility and not blocking_pairs[i]) or (
                    set(feasibility[0]) == blocking_pairs[i])
            
