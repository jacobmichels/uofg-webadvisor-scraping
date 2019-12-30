from getWatchingList import getList
import grabCourses
from subprocess import Popen
import threading
import time

#all_courses=grabCourses.fetchAll("W20") #TODO maybe make another fetchAll method that grabs all the courses from every current term. could use existing methods and do this quite easily

while(1):
    course_list=getList("watching.txt")
    for course in course_list:
        #print(course)
        course=course.split("*")
        x = threading.Thread(target=grabCourses.fetchOneSection,args=(course[0],course[1],course[2],course[3]))
        x.start()
        #Popen("python3 test.py "+course[0]+" "+course[1]+" "+course[2]+" "+course[3],shell=True)
    
    time.sleep(15)
