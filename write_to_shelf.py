import shelve
from threading import Lock

def write(key,value):
    mutex=Lock()
    try:
        mutex.acquire()
        print("Blocking...")
        db = shelve.open("shelf")
        db[key]=value
        db.close()
        mutex.release()
        print("Released!")
    except:
        print("An error occured, trying again.")
        write(key,value)
        print("Error handled.")
    finally:
        if mutex.locked:
            mutex.release
def init(name):
    shelve.open