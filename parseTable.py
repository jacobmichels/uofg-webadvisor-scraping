import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pprint import pprint

from bs4 import BeautifulSoup

file = open("HTML.txt", "r")
source = file.read()
file.close()

soup = BeautifulSoup(source, 'html.parser')

data = []
table = soup.find('table', attrs={'class': 'mainTable'})
table_body = table.find('tbody')

rows = table_body.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [element.text.strip() for element in cols]
    data.append([element for element in cols if element]) # Get rid of empty values

pprint(data)
