import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from grabCourses import fetchAll

from bs4 import BeautifulSoup

if len(sys.argv)!=2:
    raise Exception("Incorrect number of command line arguments")

if (sys.argv[1] != "W20") and (sys.argv[1] != "F19"):
    raise Exception("Specify either W20 or F19")
print("Attempting to fetch")

dict = fetchAll(sys.argv[1])
print("Writing courses.txt...")
with open('courses.txt', 'w') as f:
    for item in dict:
        f.write("%s\n" % item)
print("File written.")
