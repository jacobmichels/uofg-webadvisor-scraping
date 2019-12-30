from selenium import webdriver
from bs4 import BeautifulSoup
import sys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time


def lookup(prefix, code, term, headless):
    if(headless):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        browser = webdriver.Chrome(chrome_options=options)
    else:
        browser = webdriver.Chrome()
    browser.get("https://webadvisor.uoguelph.ca/")
    time.sleep(3)

    assert "WebAdvisor" in browser.title

    link = browser.find_element_by_class_name("WBST_Bars")
    link.click()

    link = browser.find_element_by_xpath('//*[@id="sidebar"]/div/ul[1]/li/a')
    link.click()
    strterm = ""
    select_element = Select(browser.find_element_by_name("VAR1"))
    for terms in select_element.options:
        if str(terms.text).__contains__(term):
            strterm = terms.text
            print("Assigned")
    print(strterm)
    select_element.select_by_visible_text(strterm)

    select_element = Select(browser.find_element_by_name("LIST.VAR1_1"))
    # print([o.text for o in select_element.options])
    newPrefix = ""
    for department in select_element.options:
        # print(department.text)
        if str(department.text).__contains__(prefix):
            newPrefix = department.text
            print("Assigned")
    select_element.select_by_visible_text(newPrefix)

    select_element = Select(browser.find_element_by_name("LIST.VAR2_1"))

    if(code.startswith("1")):
        select_element.select_by_visible_text("100 - First Year")
    elif(code.startswith("2")):
        select_element.select_by_visible_text("200 - Second Year")
    elif(code.startswith("3")):
        select_element.select_by_visible_text("300 - Third Year")
    elif(code.startswith("4")):
        select_element.select_by_visible_text("400 - Fourth Year")

    course_code = browser.find_element_by_name("LIST.VAR3_1")
    course_code.send_keys(str(code)+Keys.RETURN)

    time.sleep(1)
    assert "Section Selection Results" in browser.title
    source = browser.page_source
    soup = BeautifulSoup(source, 'html.parser')
    count = 0
    opencourselist = []
    for tr in soup.find(id='GROUP_Grp_WSS_COURSE_SECTIONS').find_all('tr')[2:]:
        tds = tr.find_all('td')

        for string in tds[7].stripped_strings:
            if not repr(string).startswith("'0"):
                count += 1
                opencourselist.append(tds)

    for course in opencourselist:
        for name in course[3].stripped_strings:
            print(name)

    input("press enter to close")
    browser.quit()


def getCurrentTerms():
    browser = webdriver.Chrome()
    browser.get("https://webadvisor.uoguelph.ca/")
    time.sleep(3)

    assert "WebAdvisor" in browser.title

    link = browser.find_element_by_class_name("WBST_Bars")
    link.click()

    link = browser.find_element_by_xpath('//*[@id="sidebar"]/div/ul[1]/li/a')
    link.click()

    termlist = []
    select_element = Select(browser.find_element_by_name("VAR1"))
    for terms in select_element.options:
        if str(terms.text):
            termlist.append(terms.text[:3])
            print("Added term")
    return termlist


print("Arguments: ", end=" ")
for argument in sys.argv:
    print(argument, end=" ")
print()
headlessMode = ""
if str(sys.argv[4]) == "False":
    headlessMode = False
elif str(sys.argv[4] == "True"):
    headlessMode = True
else:
    raise Exception("argv[4] has to be either 'True' or 'False'. Was {}".format(sys.argv[4]))

lookup(sys.argv[1], sys.argv[2], sys.argv[3], headlessMode)
# print(getCurrentTerms())
