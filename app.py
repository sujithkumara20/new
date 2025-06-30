from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

browser = webdriver.Chrome()  # Make sure chromedriver is installed and in PATH

browser.get('http://www.yahoo.com')
assert 'Yahoo' in browser.title

elem = browser.find_element(By.NAME, 'p')  # 'p' is the correct name for Yahoo's search box

elem.send_keys('selenium' + Keys.RETURN)

time.sleep(10)

browser.quit()