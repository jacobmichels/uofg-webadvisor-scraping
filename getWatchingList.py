def getList(file_name):
    course_list=[]
    with open(file_name,"r") as fp:
        for line in fp:
            course_list.append(line.split("\n")[0])
    return course_list