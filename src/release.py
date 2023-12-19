from selenium import webdriver
import time
import settings
# 读取配置文件
user = settings.user
# import Edge的Service
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import json
import sys
import requests
def release(Url, Username, Password, title, content):
    ser = Service()
    ser.path = 'C:\\Users\\A2564\\AppData\\Local\\Programs\\Python\\Python311\\geckodriver.exe'
    # 连接Edge浏览器
    driver = webdriver.Firefox(service=ser)
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
    release(user["url"], user["username"], user["password"], "test", "test")