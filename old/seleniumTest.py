from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

browser = webdriver.Chrome()
browser.get("https://webadvisor.uoguelph.ca/")
time.sleep(1)

#print(browser.title)
assert "WebAdvisor" in browser.title

link = browser.find_element_by_class_name("WBST_Bars")
link.click()
#print(browser.title)
# elem.send_keys("selenium"+Keys.RETURN)

link = browser.find_element_by_xpath('//*[@id="sidebar"]/div/ul[1]/li/a')
link.click()

select_element = Select(browser.find_element_by_name("VAR1"))
# print([o.text for o in select_element.options])
select_element.select_by_visible_text("F19 - Fall 2019")

select_element = Select(browser.find_element_by_name("LIST.VAR1_1"))
# print([o.text for o in select_element.options])
select_element.select_by_visible_text("CIS - Computing & Information Sci.")

select_element = Select(browser.find_element_by_name("LIST.VAR2_1"))
select_element.select_by_visible_text("200 - Second Year")

course_code = browser.find_element_by_name("LIST.VAR3_1")
#course_code.send_keys("2750"+Keys.RETURN)
course_code.send_keys("2750")

input("press enter to exit")
browser.quit()
