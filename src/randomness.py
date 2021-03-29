from compare_asp import parse_answers
from os.path import isfile

def parse_match(line):
    if line.startswith("solutions: 0"):
        return set()
    return set(line.split())

if __name__ == '__main__':
    folder = "1stmax"
    for size in [20, 40, 60, 80, 100]:
        for density in [25, 50, 75, 100]:
            print(size, density)
            file1 = "C:\\Users\\Sofia\\Documents\\level5project\\SRI_IP\\data\\outputs\\%s\\%s-SRI\\output-%s-%d-%d.txt" %("CP_new", folder, folder, size,density)
            file2 = "C:\\Users\\Sofia\\Documents\\level5project\\SRI_IP\\data\\outputs\\%s\\%s-SRI\\output-%s-%d-%d.txt" %("IP", folder, folder, size,density)
            with open(file1) as f1:
                with open(file2) as f2:
                    while not f1.readline().startswith("Instance"):
                        continue
                    while not f2.readline().startswith("Instance"):
                        continue
                    match1line = f1.readline()
                    match2line = f2.readline()
                    if match1line != match2line:
                       assert parse_match(match1line) == parse_match(match2line), (match1line, match2line)

