from compare_asp import parse_answers
from os.path import isfile

if __name__ == '__main__':

    for folder in ['almost', '', 'rankmax', 'egal']:
        for size in [20, 40, 60, 80, 100, 150, 200]:
            for density in range(25, 101, 25):
                if folder != '':
                    infix = '-' + folder
                    folder_ = folder + '-'
                else:
                    infix = ''
                    folder_ = ''
                file_name = "C:\\Users\\Sofia\\Documents\\level5project\\SRI_IP\\data\\outputs\\ASP\\%sSRI\\output%s-%d-%d.txt" % (folder_, infix, size,density)
                if not isfile(file_name):
                    file_name = "C:\\Users\\Sofia\\Documents\\level5project\\SRI_IP\\data\\outputs\\ASP\\%sSRI\\output%s-time-%d-%d.txt" % (folder_, infix, size,density)
                if not isfile(file_name) and folder == 'rankmax':
                    file_name = "C:\\Users\\Sofia\\Documents\\level5project\\SRI_IP\\data\\outputs\\ASP\\%sSRI\\output-rank-%d-%d.txt" % (folder_, size,density)
                try:
                    with open(file_name) as f_in:
                        with open(file_name.split(".txt")[0] + "_numbered.txt", "w") as f_out:
                            i = 1
                            for line in f_in.readlines():
                                if line.startswith("clingo version"):
                                    f_out.write("Instance %d\n" % i)
                                    i += 1
                                f_out.write(line)
                except FileNotFoundError:
                    print(file_name, "not found")
