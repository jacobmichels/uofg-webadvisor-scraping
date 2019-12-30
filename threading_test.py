import threading
import grabCourses

x=threading.Thread(target=grabCourses.fetchOne,args=("CIS","1500","W20"))
x.start()