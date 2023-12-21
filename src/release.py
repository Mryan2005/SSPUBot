from selenium import webdriver
import time
import sys
#import settings
# 读取配置文件
#user = settings.user
# import Edge的Service
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from pyvirtualdisplay import Display
from selenium.webdriver.common.by import By
import json

import requests
def release(Url, Username, Password, title, content):
    #display = Display(visible=0, size=(1280, 768))
    #display.start()
    ser = Service()
    ser.path = 'C:\\Users\\A2564\\AppData\\Local\\Programs\\Python\\Python311\\geckodriver.exe'
    # 连接Edge浏览器
    firefox_options = Options()
    firefox_options.add_argument("-headless")
    driver = webdriver.Firefox(options=firefox_options, service=ser)
    driver.get(Url)
    loginTag = driver.find_element(By.CLASS_NAME, "item-logIn")
    loginTag.click()
    inputTag = driver.find_element(By.NAME, "identification")
    inputTag.send_keys(Username)
    inputTag = driver.find_element(By.NAME, "password")
    inputTag.send_keys(Password)
    loginTag = driver.find_element(By.XPATH, "//button[@type='submit']")
    loginTag.click()
    time.sleep(60)
    releaseTag = driver.find_element(By.XPATH, "//button[@class=\"Button Button--primary IndexPage-newDiscussion hasIcon\"]")
    releaseTag.click()
    inputTag = driver.find_element(By.XPATH, "//input[@placeholder=\"标题\"]")
    inputTag.send_keys(title)
    inputTag = driver.find_element(By.XPATH, "//textarea[@class=\"FormControl Composer-flexible TextEditor-editor\"]")
    inputTag.send_keys(content)
    releaseTag = driver.find_element(By.XPATH, "//button[@class=\"Button Button--primary hasIcon\"]")
    releaseTag.click()
    time.sleep(60)
    primaryTag = driver.find_element(By.XPATH, "//i[@class=\"icon fas fa-bug\"]")
    primaryTag.click()
    suubmitTag = driver.find_element(By.XPATH, "//div[@class=\"TagSelectionModal-form-submit App-primaryControl\"]")
    suubmitTag.click()
    driver.close()
if __name__ == "__main__":  
    release(sys.argv[3], sys.argv[4], sys.argv[5], "test", "test")