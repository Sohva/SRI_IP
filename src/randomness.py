from compare_asp import parse_answers
from os.path import isfile

if __name__ == '__main__':

    for size in [20, 40, 60, 80, 100, 150, 200]:
        for density in range(25, 101, 25):
            for i in range(1, 21):
                file_name = "C:\\Users\\Sofia\\Documents\\level5project\\SRI_IP\\data\\instances\\%d\\i-%d-%d-%d.txt" % (size, size,density, i)
                with open(file_name) as f_in:
                    with open(file_name.split(".txt")[0] + "_numbered.txt", "w") as f_out:
                        for j, line in enumerate(f_in.readlines()):
                            if j != 0:
                                line = str(j) + " : " + line
                            f_out.write(line)
