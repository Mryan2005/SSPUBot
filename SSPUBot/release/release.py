import platform
import sys
import time

import selenium.common.exceptions
# import settings
# 读取配置文件
# user = settings.user
# import Edge的Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service


def release(Url, Username, Password, title, content):
    # display = Display(visible=0, size=(1280, 768))
    # display.start()
    ser = Service()
    if (platform.system() == "Windows"):
        ser.path = 'C:\\Users\\A2564\\AppData\\Local\\Programs\\Python\\Python311\\geckodriver.exe'
    elif (platform.system() == "Linux"):
        ser.path = './geckodriver'
    # 连接Edge浏览器
    firefox_options = Options()
    if sys.argv[0] == "normal":
        firefox_options.add_argument("-headless")
    elif sys.argv[0] == "test":
        pass
    driver = webdriver.Firefox(options=firefox_options, service=ser)
    driver.get(Url)
    time.sleep(3)
    loginTag = driver.find_element(By.CLASS_NAME, "item-logIn")
    loginTag.click()
    inputTag = driver.find_element(By.NAME, "identification")
    inputTag.send_keys(Username)
    inputTag = driver.find_element(By.NAME, "password")
    inputTag.send_keys(Password)
    time.sleep(3)
    loginTag = driver.find_element(By.XPATH, "//button[@type='submit']")
    loginTag.click()
    time.sleep(10)
    try:
        if (Url == "https://forum.akiacg.com"):
            releaseTag = driver.find_element(By.XPATH,
                                             "//button[@class=\"Button Button--primary IndexPage-newDiscussion hasIcon\"]")
        elif (Url == "https://akiacgdx.flarum.cloud"):
            releaseTag = driver.find_element(By.XPATH, "//button[@itemclassname=\"App-primaryControl\"]")
        releaseTag.click()
    except selenium.common.exceptions.NoSuchElementException:
        driver.refresh()
        loginTag = driver.find_element(By.CLASS_NAME, "item-logIn")
        loginTag.click()
        inputTag = driver.find_element(By.NAME, "identification")
        inputTag.send_keys(Username)
        inputTag = driver.find_element(By.NAME, "password")
        inputTag.send_keys(Password)
        time.sleep(3)
        loginTag = driver.find_element(By.XPATH, "//button[@type='submit']")
        loginTag.click()
        time.sleep(10)
        if (Url == "https://forum.akiacg.com"):
            releaseTag = driver.find_element(By.XPATH,
                                             "//button[@class=\"Button Button--primary IndexPage-newDiscussion hasIcon\"]")
        elif (Url == "https://akiacgdx.flarum.cloud"):
            releaseTag = driver.find_element(By.XPATH, "//button[@itemclassname=\"App-primaryControl\"]")
        releaseTag.click()
    inputTag = driver.find_element(By.XPATH, "//input[@placeholder=\"标题\"]")
    inputTag.send_keys(title)
    time.sleep(5)
    inputTag = driver.find_element(By.XPATH, "//textarea[@class=\"FormControl Composer-flexible TextEditor-editor\"]")
    inputTag.send_keys(content)
    time.sleep(3)
    releaseTag = driver.find_element(By.XPATH, "//button[@class=\"Button Button--primary hasIcon\"]")
    releaseTag.click()
    time.sleep(60)
    if (Url == "https://forum.akiacg.com"):
        primaryTag = driver.find_element(By.XPATH, "//i[@class=\"icon fas fa-info\"]")
    elif (Url == "https://akiacgdx.flarum.cloud"):
        primaryTag = driver.find_element(By.XPATH, "//i[@class=\"icon fas fa-bullhorn\"]")
    primaryTag.click()
    suubmitTag = driver.find_element(By.XPATH, "//div[@class=\"TagSelectionModal-form-submit App-primaryControl\"]")
    suubmitTag.click()
    time.sleep(5)
    driver.close()


if __name__ == "__main__":
    file = open("result.md", "r")
    content = file.read()
    file.close()
    release(s.user["url"], s.user["username"], s.user["password"], "test", content)
