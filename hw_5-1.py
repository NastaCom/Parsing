from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import date
import time
from pprint import pprint
from pymongo import MongoClient

driver = webdriver.Chrome('chromedriver.exe')

driver.get('https://mail.ru/')

elem = driver.find_element(By.NAME, 'login')
elem.send_keys('study.ai_172@mail.ru')
#elem.send_keys('study.ai_172@mail.ru')
elem.send_keys(Keys.ENTER)
elem.click()

elem = driver.find_element(By.NAME, 'password')
elem.send_keys('NextPassword172#')

#elem.send_keys('NextPassword172#')  //input[@class="password-input svelte-1tib0qz"]
elem.send_keys(Keys.ENTER)

time.sleep(10)
link_lists = []
number_of_letters = 0
while True:
    mail_items = driver.find_element_by_xpath('//a[@data-id]')
    for item in mail_items:
        link = item.get_property('href')
        link_lists.append(link)
    link_lists = list(set(link_lists))

    if number_of_letters == len(mail_items):
        break
    else:
        number_of_letters = len(mail_items)
    down = mail_items[-1].send_keys(Keys.PAGE_DOWN)

pprint(link_lists)
pprint(len(link_lists))



letters = []
for link in link_lists:
    driver.get(link)
    time.sleep(4)
    from_element = driver.find_element_by_class_name('letter-contact')
    subject_element = driver.find_element_by_class_name('thread__subject')
    time_element = driver.find_element_by_class_name('letter__date')
    text_element = driver.find_element_by_class_name('letter-body__body-content')
    time.sleep(2)

    letter = {}
    letter['from'] = from_element.text
    letter['subject'] = subject_element.text
    letter['text'] = text_element.text
    letter['time'] = time_element.text
    letters.append(letter)

pprint(letters)
driver.close()


client = MongoClient('localhost', 27017)
db = client['mail-ru']
collection = db.test_collection
collection.insertMany(letters)
