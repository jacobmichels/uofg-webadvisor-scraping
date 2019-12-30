import sys
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
browser = webdriver.Chrome(chrome_options=options)
browser.get("https://webadvisor.uoguelph.ca/")
delay = 3  # seconds

term = "W20"

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

except TimeoutException:
    print("Loading took too much time!")

source = browser.page_source
browser.quit()
print("Writing HTML.")
file = open("HTML.txt", "w")
file.write(source)
file.close()
print("Done.")
