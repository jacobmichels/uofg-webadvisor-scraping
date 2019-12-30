from bs4 import BeautifulSoup
from collections import OrderedDict
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import shelve
import sys
import threading
import write_to_shelf


def fetchAll(term):
    #db = shelve.open("shelf")
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(chrome_options=options)
    browser.get("https://webadvisor.uoguelph.ca/")
    delay = 3  # seconds
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'WBST_Bars')))
        print("Homepage is ready!")
        myElem.click()

        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH,'//*[@id="sidebar"]/div/ul[1]/li/a')))
        print("Student page is ready!")
        myElem.click()

        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.NAME,'VAR1')))
        strterm = ""
        select_element = Select(browser.find_element_by_name("VAR1"))
        for terms in select_element.options:
            if str(terms.text).__contains__(term):
                strterm = terms.text
                print("Assigned term = {}".format(strterm))
        select_element.select_by_visible_text(strterm)

        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.NAME,'VAR6')))
        select_element = Select(browser.find_element_by_name('VAR6')).select_by_visible_text('G - Guelph')    #only get courses that are held on guelph campus

        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.NAME,'VAR21')))
        select_element = Select(browser.find_element_by_name('VAR21')).select_by_visible_text('UG - Undergraduate')   #only get undergrad courses, for now?

        print("Requesting course data")
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.NAME,'SUBMIT2'))).click()
        print("Fetched all course data.")
        print("Parsing HTML, this might take a few seconds...")

    except TimeoutException:
        print("Loading took too much time!")
        exit(-1)

    source = browser.page_source
    browser.quit()
    soup = BeautifulSoup(source, 'html.parser')

    courseDict = {}
    courseNameRaw = ""
    slots=""
    faculty=""
    credit=""
    for tr in soup.find(id='GROUP_Grp_WSS_COURSE_SECTIONS').find_all('tr')[2:]:
        tds = tr.find_all('td')
        for name in tds[3].stripped_strings:     #this loop only executes once.
            courseNameRaw = name            
        for availability in tds[7].stripped_strings:
            slots = availability
        for teacher in tds[6].stripped_strings:
            faculty = teacher
        for creditAmount in tds[8].stripped_strings:
            credit = creditAmount
        #print(courseNameRaw)
        courseNameTokenized = courseNameRaw.split(" ")[0]
        courseID = courseNameRaw.split(" ")[1]
        #print(courseNameTokenized+" "+courseID)
        courseInfoList = []
        courseInfoList.append(courseID)
        courseInfoList.append(slots)
        courseInfoList.append(faculty)
        courseInfoList.append(credit)
        courseDict[courseNameTokenized+"*"+term]=courseInfoList
        #write_to_shelf.write(courseNameTokenized+"*"+term,courseInfoList)
        x=threading.Thread(target=write_to_shelf.write,args=(courseNameTokenized+"*"+term,courseInfoList))
        x.start()
        #db[courseNameTokenized+"*"+term]=courseInfoList
        

    #db.close()
    print("Courses returned.")
    return courseDict


def fetchOne(department, code, term):
    print("Course: {} {} Term: {}".format(department, code, term))
    #db = shelve.open("shelf")
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(chrome_options=options)
    browser.get("https://webadvisor.uoguelph.ca/")
    delay = 3  # seconds
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'WBST_Bars')))
        print("Homepage is ready!")
        myElem.click()

        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH,'//*[@id="sidebar"]/div/ul[1]/li/a')))
        print("Student page is ready!")
        myElem.click()

        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.NAME,'VAR1')))
        strterm = ""
        select_element = Select(browser.find_element_by_name("VAR1"))
        for terms in select_element.options:
            if str(terms.text).__contains__(term):
                strterm = terms.text
                print("Assigned term = {}".format(strterm))
        select_element.select_by_visible_text(strterm)

        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.NAME,'VAR6')))
        select_element = Select(browser.find_element_by_name('VAR6')).select_by_visible_text('G - Guelph')    #only get courses that are held on guelph campus

        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.NAME,'VAR21')))
        select_element = Select(browser.find_element_by_name('VAR21')).select_by_visible_text('UG - Undergraduate')   #only get undergrad courses, for now?

        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID,'LIST_VAR1_1')))
        select_element = Select(browser.find_element_by_id("LIST_VAR1_1"))
        strDepartment = ""
        for departments in select_element.options:
            if str(departments.text).__contains__(department):
                strDepartment = departments.text
                print("Assigned term = {}".format(strDepartment))
        select_element.select_by_visible_text(strDepartment)

        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.NAME,'LIST.VAR2_1')))
        select_element = Select(browser.find_element_by_name('LIST.VAR2_1'))
        if(code.startswith("1")):
            select_element.select_by_visible_text("100 - First Year")
        elif(code.startswith("2")):
            select_element.select_by_visible_text("200 - Second Year")
        elif(code.startswith("3")):
            select_element.select_by_visible_text("300 - Third Year")
        elif(code.startswith("4")):
            select_element.select_by_visible_text("400 - Fourth Year")

        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.NAME,'LIST.VAR3_1')))
        myElem.send_keys(str(code)+Keys.RETURN)
    except TimeoutException:
        print("Loading took too much time!")
        exit(-1)
    
    source = browser.page_source
    browser.quit()
    soup = BeautifulSoup(source, 'html.parser')

    courseDict = {}
    threadList=[]
    courseNameRaw = ""
    slots=""
    faculty=""
    credit=""
    for tr in soup.find(id='GROUP_Grp_WSS_COURSE_SECTIONS').find_all('tr')[2:]:
        tds = tr.find_all('td')
        for name in tds[3].stripped_strings:     #this loop only executes once.
            courseNameRaw = name            
        for availability in tds[7].stripped_strings:
            slots = availability
        for teacher in tds[6].stripped_strings:
            faculty = teacher
        for creditAmount in tds[8].stripped_strings:
            credit = creditAmount
        #print(courseNameRaw)
        courseNameTokenized = courseNameRaw.split(" ")[0]
        courseID = courseNameRaw.split(" ")[1]
        #print(courseNameTokenized+" "+courseID)
        courseInfoList = []
        courseInfoList.append(courseID)
        courseInfoList.append(slots)
        courseInfoList.append(faculty)
        courseInfoList.append(credit)
        courseDict[courseNameTokenized+"*"+term]=courseInfoList
        x=threading.Thread(target=write_to_shelf.write,args=(courseNameTokenized+"*"+term,courseInfoList))
        threadList.append(x)
        #write_to_shelf.write(courseNameTokenized+"*"+term,courseInfoList)
        #db[courseNameTokenized+"*"+term]=courseInfoList

    for x in threadList:
        x.start()

    #db.close()
    for x in threadList:
        x.join()
    print("Courses returned.")
    return courseDict


def fetchOneSection(department, code, section, term):
    print(department+" "+code+"*"+section+" "+term)
    #db = shelve.open("shelf")
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(chrome_options=options)
    browser.get("https://webadvisor.uoguelph.ca/")
    delay = 3  # seconds
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'WBST_Bars')))
        print("Homepage is ready!")
        myElem.click()

        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH,'//*[@id="sidebar"]/div/ul[1]/li/a')))
        print("Student page is ready!")
        myElem.click()

        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.NAME,'VAR1')))
        strterm = ""
        select_element = Select(browser.find_element_by_name("VAR1"))
        for terms in select_element.options:
            if str(terms.text).__contains__(term):
                strterm = terms.text
                print("Assigned term = {}".format(strterm))
        select_element.select_by_visible_text(strterm)

        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.NAME,'VAR6')))
        select_element = Select(browser.find_element_by_name('VAR6')).select_by_visible_text('G - Guelph')    #only get courses that are held on guelph campus

        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.NAME,'VAR21')))
        select_element = Select(browser.find_element_by_name('VAR21')).select_by_visible_text('UG - Undergraduate')   #only get undergrad courses, for now?

        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID,'LIST_VAR1_1')))
        select_element = Select(browser.find_element_by_id("LIST_VAR1_1"))
        strDepartment = ""
        for departments in select_element.options:
            if str(departments.text).__contains__(department):
                strDepartment = departments.text
                print("Assigned term = {}".format(strDepartment))
        select_element.select_by_visible_text(strDepartment)

        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.NAME,'LIST.VAR2_1')))
        select_element = Select(browser.find_element_by_name('LIST.VAR2_1'))
        if(code.startswith("1")):
            select_element.select_by_visible_text("100 - First Year")
        elif(code.startswith("2")):
            select_element.select_by_visible_text("200 - Second Year")
        elif(code.startswith("3")):
            select_element.select_by_visible_text("300 - Third Year")
        elif(code.startswith("4")):
            select_element.select_by_visible_text("400 - Fourth Year")

        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.NAME,'LIST.VAR3_1')))
        myElem.send_keys(str(code))

        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.NAME,'LIST.VAR4_1')))
        myElem.send_keys(str(section)+Keys.RETURN)
    except TimeoutException:
        print("Loading took too much time!")
        exit(-1)
    
    source = browser.page_source
    browser.quit()
    soup = BeautifulSoup(source, 'html.parser')

    courseDict = {}
    courseNameRaw = ""
    slots=""
    faculty=""
    credit=""
    for tr in soup.find(id='GROUP_Grp_WSS_COURSE_SECTIONS').find_all('tr')[2:]:
        tds = tr.find_all('td')
        for name in tds[3].stripped_strings:     #this loop only executes once.
            courseNameRaw = name            
        for availability in tds[7].stripped_strings:
            slots = availability
        for teacher in tds[6].stripped_strings:
            faculty = teacher
        for creditAmount in tds[8].stripped_strings:
            credit = creditAmount
        #print(courseNameRaw)
        courseNameTokenized = courseNameRaw.split(" ")[0]
        courseID = courseNameRaw.split(" ")[1]
        #print(courseNameTokenized+" "+courseID)
        courseInfoList = []
        courseInfoList.append(courseID)
        courseInfoList.append(slots)
        courseInfoList.append(faculty)
        courseInfoList.append(credit)
        courseDict[courseNameTokenized+"*"+term]=courseInfoList
        x=threading.Thread(target=write_to_shelf.write,args=(courseNameTokenized+"*"+term,courseInfoList))
        x.start()
        #write_to_shelf.write(courseNameTokenized+"*"+term,courseInfoList)
        #db[courseNameTokenized+"*"+term]=courseInfoList


    #db.close()
    print("Courses returned.")
    return courseDict
