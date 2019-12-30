import grabCourses
from pprint import pprint

func = int(input("What function to run?\n1: FetchOne\n2: FetchOneSection\n3: FetchAll\n"))
if not (func == 1 or func == 2 or func == 3):
    raise Exception("Invalid function number.")
    exit(-1)

if func == 1:
    parameters_raw = str(input("Enter department, code, and term separated by spaces\n"))
    parameters = parameters_raw.split(" ")
    if not len(parameters) == 3:
        raise Exception("Invalid number of arguments entered.")
        exit(-1)
    pprint(grabCourses.fetchOne(parameters[0], parameters[1], parameters[2]))

if func == 2:
    parameters_raw = str(input("Enter department, code, section number, and term separated by spaces\n"))
    parameters = parameters_raw.split(" ")
    if not len(parameters) == 4:
        raise Exception("Invalid number of arguments entered.")
        exit(-1)
    pprint(grabCourses.fetchOneSection(parameters[0], parameters[1], parameters[2], parameters[3]))

if func == 3:
    parameter = str(input("Enter the term to get all courses for\n"))
    if not len(parameter) == 3:
        raise Exception("Term is not 3 characters.")
        exit(-1)
    pprint(grabCourses.fetchAll(parameter))
