from compare_asp import parse_answers
from feasibility_checker import check_feasibility
from utils import read_instance

if __name__ == "__main__":
    size = 40
    density = 25
    file = "C:\\Users\\Sofia\\Documents\\level5project\\SRI_IP\\data\\outputs\\ASP\\almost-SRI\\output-almost-%d-%d.txt" % (size, density)
    answers = parse_answers(file, True)
    file_base = "C:\\Users\\Sofia\\Documents\\level5project\\SRI_IP\\data\\instances\\%d\\i-%d-%d-%d.txt"
    for i, ans in enumerate(answers):
        answer, blocking = ans
        preferences = read_instance(file_base % (size, size, density, i+1), 0)
        print(i+1)
        print(check_feasibility(preferences, answer))
        print(blocking)
        print()
        
