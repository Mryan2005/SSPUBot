# -*- coding: utf-8 -*-
# Function: get the information from the school website and the official account
# Path: SSPUBot/getInformation/getInformation.py
# Compare this snippet from SSPUBot/release/release.py:
import io
import json
import logging
import os
import pickle
import sys
import time
import urllib.request

import requests
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from seleniumwire import webdriver
from seleniumwire.webdriver import Firefox

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename="./data/log.txt", filemode='w+')  # 日志配置
try:
    if sys.argv[1] == "onDocker":
        ser = Service("./geckodriver")
except IndexError:
    ser = Service()
firefox_options = Options()
# firefox_options.add_argument('--ignore-certificate-errors')
# firefox_options.add_argument('--proxy-server={0}'.format(proxy.proxy))
try:
    if sys.argv[1] == "onDocker":
        firefox_options.add_argument('--headless')
        firefox_options.add_argument('--disable-gpu')
except IndexError:
    pass
logging.info("正在启动浏览器Firefox")
driver: Firefox = webdriver.Firefox(options=firefox_options, service=ser)  # connect to the browser
driver.set_page_load_timeout(30)  # set the time to load the page
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')  # set the output encoding
try:
    logging.info("正在读取设置")
    settings = json.load(open("../data/settings/settings.json", "r", encoding="utf-8"))
    logging.info("读取设置成功")
except FileNotFoundError:
    logging.warning("读取设置失败, 正在寻找其他地方")
    settings = json.load(open("./data/settings/settings.json", "r", encoding="utf-8"))
    logging.info("读取设置成功")
except UnicodeDecodeError:
    logging.warning("编码错误")
    try:
        settings = json.load(open("../data/settings/settings.json", "r", encoding="GBK"))
        logging.info("读取设置成功")
    except FileNotFoundError:
        settings = json.load(open("./data/settings/settings.json", "r", encoding="GBK"))
        logging.info("读取设置成功")

# read the settings
websites = settings["websites"]
# define the driver
logging.info("正在启动浏览器")


def releaseWechatAccountOverdueNotice():
    session = requests.Session()
    logging.info("Release start!")
    logging.info("正在尝试连接到服务器...")
    responses = session.get(settings["url"])
    head = {
        "Accept": "application/vnd.api+json",
        "Content-Type": "application/vnd.api+json",
        "Authorization": "Token " + settings["token"]
    }
    id = 19
    data = {
        "data": {
            "type": "discussions",
            "attributes": {
                "title": "微信公众号登录过期通知",
                "content": "您的微信公众号登录已经过期"
            },
            "relationships": {
                "tags": {
                    "data": [
                        {
                            "type": "tags",
                            "id": id
                        }
                    ]
                }
            }
        }
    }
    responses = session.post(settings["url"] + "/api/discussions", headers=head, json=data)
    if responses.status_code == 201:
        print("Release success!")
        logging.info("Release" + "微信公众号过期通知" + " success!")
    else:
        print("Release failed!")
        print(responses.status_code)
        logging.error("Release" + "微信公众号过期通知" + " failed!")
        logging.error(str(responses.status_code) + " " + str(responses.content))
    logging.info("Release end!")


# define the classes
# define the Error
class notLoginError(Exception):
    def __init__(self, ErrorInfo):
        super().__init__(self, ErrorInfo)
        self.errorinfo = ErrorInfo

    def __str__(self):
        return self.errorinfo


class noScanQRCodeError(Exception):
    def __init__(self):
        super().__init__(self)
        self.errorinfo = "没有扫码"

    def __str__(self):
        return self.errorinfo


# define the post class
class Post(object):
    def __init__(self):
        self.outline = None
        self.file = None
        self.url = None
        self.title = None
        self.source = None

    def setTitle(self, title):
        self.title = title

    def setUrl(self, url):
        self.url = url

    def setOutline(self, outline):
        self.outline = outline

    def setSource(self, source):
        self.source = source


# define the function to make error
def MakeErrorAboutNoLogin():
    raise notLoginError("如登")


def MakeErrorAboutNoScanQRCode():
    raise noScanQRCodeError()


def MakeErrorAboutTimeout():
    raise TimeoutError("超时")


posts = []


# define the function to check the word
def is_word_which_i_need(chars):
    for i in chars:
        if '\u4e00' <= i <= '\u9fff':
            return True
        elif '0' <= i <= '9':
            return True
        elif '-' == i:
            return True
        else:
            return False


# define the login function
def login():
    try:
        # login with cookies
        logging.info("正在读取cookies")
        cookies = pickle.load(open("./data/wechat_cookies.pkl", "rb"))
        for cookie in cookies:
            if isinstance(cookie.get('expiry'), float):
                cookie['expiry'] = int(cookie['expiry'])
            driver.add_cookie(cookie)
        driver.refresh()
        writeafile = driver.find_elements(By.XPATH, "//div[@class=\"new-creation__menu-title\"]")
        if len(writeafile) == 0:
            MakeErrorAboutNoLogin()
            logging.warning("cookies没有内容，正在重新登录")
    except FileNotFoundError:
        logging.warning("cookies文件不存在，正在重新登录")
        # login with username and password
        LoginTag = driver.find_element(By.XPATH, "//a[@class=\"login__type__container__select-type\"]")
        LoginTag.click()
        UserNameTag = driver.find_element(By.XPATH, "//input[@name=\"account\"]")
        UserNameTag.send_keys(settings["weixinUsername"])
        PasswordTag = driver.find_element(By.XPATH, "//input[@name=\"password\"]")
        PasswordTag.send_keys(settings["weixinPassword"])
        LoginTag = driver.find_element(By.XPATH, "//a[@class=\"btn_login\"]")
        LoginTag.click()
        logging.info("正在等待扫码码")
        try:
            if sys.argv[1] == "onDocker":
                time.sleep(10)
                driver.save_screenshot("./data/QRCode.png")
        except IndexError:
            pass
        time.sleep(120)
        cookie = driver.get_cookies()
        pickle.dump(cookie, open('./data/wechat_cookies.pkl', 'wb'))
        driver.refresh()
    except notLoginError or IndexError:
        logging.warning("cookies失效，正在重新登录")
        # login with username and password if the cookies are wrong
        driver.delete_all_cookies()
        LoginTag = driver.find_element(By.XPATH, "//a[@class=\"login__type__container__select-type\"]")
        LoginTag.click()
        UserNameTag = driver.find_element(By.XPATH, "//input[@name=\"account\"]")
        UserNameTag.send_keys(settings["weixinUsername"])
        PasswordTag = driver.find_element(By.XPATH, "//input[@name=\"password\"]")
        PasswordTag.send_keys(settings["weixinPassword"])
        LoginTag = driver.find_element(By.XPATH, "//a[@class=\"btn_login\"]")
        LoginTag.click()
        logging.info("正在等待扫码码")
        try:
            if sys.argv[1] == "onDocker":
                time.sleep(10)
                driver.save_screenshot("./data/QRCode.png")
        except IndexError:
            pass
        time.sleep(120)
        cookie = driver.get_cookies()
        pickle.dump(cookie, open('./data/wechat_cookies.pkl', 'wb'))
        driver.refresh()


# define the function to get the official account information
def GetOfficialAccount(accountName, posts, k, lastpart):
    time.sleep(3)
    # define some values
    writeafile = []
    openingTag = []
    try:
        logging.info("正在创建新的图文消息")
        writeafile = driver.find_elements(By.XPATH, "//div[@class=\"new-creation__menu-title\"]")
    except selenium.common.exceptions.NoSuchElementException:
        time.sleep(30)
        writeafile = driver.find_elements(By.XPATH, "//div[@class=\"new-creation__menu-title\"]")
    try:
        writeafile[0].click()
    except IndexError:
        try:
            logging.error("二维码未扫描，正在等待下一次运行")
            settingsNew = json.load(open("../data/settings/settings.json", "r", encoding="utf-8"))
            settingsNew["isLogin"] = False
            json.dump(settingsNew, open("../data/settings/settings.json", "w", encoding="utf-8"))
            try:
                if sys.argv[1] == "onDocker":
                    os.system("pkill -9 firefox")
                    os.system("pkill -9 firefox-bin")
            except IndexError:
                pass
        except FileNotFoundError:
            settingsNew = json.load(open("./data/settings/settings.json", "r", encoding="utf-8"))
            settingsNew["isLogin"] = False
            json.dump(settingsNew, open("./data/settings/settings.json", "w", encoding="utf-8"))

            try:
                if sys.argv[1] == "onDocker":
                    os.system("pkill -9 firefox")
                    os.system("pkill -9 firefox-bin")
            except IndexError:
                pass
        releaseWechatAccountOverdueNotice()
        exit(1)
    time.sleep(5)
    windows = driver.window_handles
    logging.info("正在选择图文消息的标签页")
    driver.switch_to.window(windows[-1])
    time.sleep(3)
    try:
        logging.info("正在选择内链")
        openingTag = driver.find_element(By.XPATH, "//li[@id=\"js_editor_insertlink\"]")
    except selenium.common.exceptions.NoSuchElementException:
        logging.warning("网站未加载完成，正在等待30秒")
        time.sleep(30)
        openingTag = driver.find_element(By.XPATH, "//li[@id=\"js_editor_insertlink\"]")
    finally:
        logging.info("正在点击内链")
        openingTag.click()
        time.sleep(3)
    del driver.requests
    # get the url of the official account
    logging.info("正在获取公众号的url")
    openingTag = driver.find_elements(By.XPATH, "//button[@class=\"weui-desktop-btn weui-desktop-btn_default\"]")
    openingTag[0].click()
    inputtingTag = driver.find_elements(By.XPATH, "//input[@class=\"weui-desktop-form__input\"]")
    inputtingTag[1].send_keys(accountName)
    searchingTag = driver.find_elements(By.XPATH, "//button[@class=\"weui-desktop-icon-btn weui-desktop-search__btn\"]")
    searchingTag[0].click()
    time.sleep(5)
    selectingTag = driver.find_elements(By.XPATH, "//li[@class=\"inner_link_account_item\"]")
    selectingTag[0].click()
    # get the url of the official account
    time.sleep(3)
    requestList = driver.requests
    url = ""
    for i in requestList:
        if "mp.weixin.qq.com" in i.url:
            if "cgi-bin/appmsgpublish?sub=list&search_field=null" in i.url:
                if not ('&query=&fakeid=&' in i.url):
                    url = i.url
                    break
    if str(url) == '':
        driver.close()
        driver.switch_to.window(windows[0])
        logging.error("无法获取url，正在等待下一次运行")
        return 1
    logging.info("正在获取公众号的url成功, url为" + url + ", 正在获取公众号的文章")
    try:
        driver.get(url)
    except selenium.common.exceptions.TImeoutException:
        logging.error("超时, 跳过")
        return 1
    time.sleep(3)
    # get the information of the official account
    htmls = driver.page_source
    htmls = htmls.replace("\\\\", "")
    text = ''
    flag = 0
    # get the title and the url of the post
    for i in htmls:
        text += i
        if '"title":"' in text:
            k += 1
            text = ''
            flag = 1
            posts.append(Post())
        if flag == 1:
            if '"' in text:
                text = text.replace('"', '')
                text = text.replace('\\\\', '')
                text = text.replace('"', '')
                outline = text.replace("²", "平方")
                print(outline)
                posts[k].setTitle(title=outline)
                flag = 2
                text = ''
        if flag == 2:
            if '"link":"' in text:
                text = ''
                flag = 3
        if flag == 3:
            if '"' in text:
                text = text.replace('"', '')
                text = text.replace('\\\\', '')
                text = text.replace('"', '')
                print(text)
                posts[k].setUrl(url=text)
                flag = 4
                text = ''
        if flag == 4:
            flag = 0
    logging.info("获取公众号的文章成功")
    # get the outline of the post
    for g in posts[lastpart + 1:]:
        try:
            url = g.url
        except AttributeError:
            g.setOutline("由于网页不支持打开，请到该站点查看")
            continue
        try:
            time.sleep(3)
            try:
                logging.info("正在进入文章的url")
                driver.get(url)
            except selenium.common.exceptions.InvalidArgumentException:
                logging.warning("网页不支持打开")
                g.setOutline("由于网页不支持打开，请到该站点查看")
            try:
                time.sleep(3)
                outlines = driver.find_elements(By.XPATH, "//section")
            except selenium.common.exceptions.NoSuchElementException:
                time.sleep(30)
                outlines = driver.find_elements(By.XPATH, "//section")
            try:
                logging.info("正在获取文章的概要")
                outline = outlines[0].text[:]
                g.setOutline(outline)
            except selenium.common.exceptions.StaleElementReferenceException:
                g.setOutline("由于网页不支持打开，请到该站点查看")
            except IndexError:
                g.setOutline("可能内容被删除了，或者这是张图片")
        except selenium.common.exceptions.NoSuchElementException:
            g.setOutline("由于网页不支持打开，请到该站点查看")
        logging.info("获取文章的概要完成")
    for g in posts[lastpart + 1:]:
        outline = g.outline
        outline = outline.replace("\n", " ")
        outline = outline.replace(" ", " ")
        outline = outline.replace("²", "平方")
        for i in settings["theSymbolThatTriggersALineBreak"]:
            outline = outline.replace(i, f"{i}\n")
        g.setOutline(outline)
        g.setSource(accountName)
    # close the page, select the first page and refresh the page.
    logging.info("正在关闭页面")
    driver.close()
    logging.info("正在切换到第一个页面")
    windows = driver.window_handles
    driver.switch_to.window(windows[0])
    driver.refresh()
    return 0


# define the function to get the information from the school website

def getSchooljwc():
    text = ''
    flag = 0
    flag1 = 0
    k = -1
    # get the information from the school website which is "jwc.sspu.edu.cn"
    logging.info("正在获取教务处的信息")
    res = urllib.request.urlopen('https://jwc.sspu.edu.cn/897/list.htm')
    htmlBytes = res.read()
    websiteResultList = open('website.html', 'wb')
    websiteResultList.write(htmlBytes)
    websiteResultList.close()
    websiteResultList = open('website.html', 'rb')
    websiteResultList.close()
    file = open('website.html', 'rb')
    file2 = open('result.txt', 'w')
    texts = file.readlines()
    file.close()
    # get the title and the url of the post ---- start
    logging.info("正在获取教务处的标题和url")
    for i in texts:
        if '<ul class="news_list list2">' in i.decode("utf8") and flag == 0:
            flag = 1
            print("find")
        if flag == 1:
            if '<span class="news_title">' in i.decode("utf8"):
                for j in i.decode("utf8"):
                    if j != '\t' and flag1 == 0:
                        text += j
                    if '<span class="news_title">' in text and flag1 == 0:
                        text = ''
                        j = ''
                        flag1 = 1
                    if flag1 == 1:
                        if j != '\n' and j != '\t':
                            text += j
                            if '</span>' in text:
                                # print(text)
                                file2.write(text)
                                file2.write('\n')
                                text = ''
                                flag1 = 0
    file2.close()
    # get the title and the url of the post ---- end
    # get the outline of the post ---- start
    logging.info("正在获取教务处文件的概要")
    text = ''
    file = open('result.txt', 'r')
    for i in file.readlines():
        k += 1
        posts.append(Post())
        for j in i:
            if j != ' ':
                text += j
            if '<a' == text:
                flag = 1
                text = ''
            if flag == 1:
                if 'href=' == text:
                    text = ''
                    flag = 2
            if flag == 2:
                if j == "'":
                    flag = 3
                    text = ''
                    continue
            if flag == 3:
                if j == "'":
                    flag = 4
                    text = text.replace("'", "", 1)
                    print("https://jwc.sspu.edu.cn" + text)
                    posts[k].setUrl("https://jwc.sspu.edu.cn" + text)
                    text = ''
            if flag == 4:
                if "target='_blank'" == text:
                    text = ''
                    flag = 5
            if flag == 5:
                if 'title=' == text:
                    text = ''
                    flag = 6
            if flag == 6:
                if j == "'":
                    flag = 7
                    text = ''
                    continue
            if flag == 7:
                if j == "'":
                    flag = 8
                    text = text.replace("'", "", 1)
                    print(text)
                    posts[k].setTitle(text)
                    print('------------------')
                    text = ''
            if flag == 8:
                flag = 0
                break
    logging.info("获取教务处文件的概要成功，正在获取教务处文件")
    oldPosts = open("../data/haveReleased.sspubot", "r+", encoding="utf-8")
    oldPostList = oldPosts.readlines()
    for g in posts:
        url = g.url
        if url in oldPostList or g.title in oldPostList:
            continue
        try:
            driver.get(url)
            outline = driver.find_element(By.XPATH, "//div[@class=\"WordSection1\"]")
            outline = outline.text[:]
            g.setOutline(outline)
        except selenium.common.exceptions.NoSuchElementException:
            g.setOutline("由于网页不支持打开，请到该站点查看")
        g.setSource("教务处")


# get the outline of the post ---- end


def getschoolpe():
    # get the information from the school website which is "pe2016.sspu.edu.cn"
    logging.info("正在获取体育部的信息")
    # define some values ---- start
    lastpart = len(posts) - 1
    text = ''
    flag = 0
    flag1 = 0
    # define some values ---- end
    # get the title and the url of the post
    logging.info("正在获取体育部的标题和url")
    res = urllib.request.urlopen('https://pe2016.sspu.edu.cn/342/list.htm')
    htmlBytes = res.read()
    websiteResultList = open('website.html', 'wb')
    websiteResultList.write(htmlBytes)
    websiteResultList.close()
    websiteResultList = open('website.html', 'rb')
    websiteResultList.close()
    file = open('website.html', 'rb')
    file2 = open('result.txt', 'w')
    texts = file.readlines()
    file.close()
    for i in texts:
        if '<div class="dht_blank1"></div>' in i.decode("utf8") and flag == 0:
            flag = 1
            print("find")
        if flag == 1:
            if '<li>' in i.decode("utf8"):
                for j in i.decode("utf8"):
                    if j != '\t' and flag1 == 0:
                        text += j
                    if '<li>' in text and flag1 == 0:
                        text = ''
                        j = ''
                        flag1 = 1
                    if flag1 == 1:
                        if j != '\n' and j != '\t':
                            text += j
                            if '</li>' in text:
                                # print(text)
                                file2.write(text)
                                file2.write('\n')
                                text = ''
                                flag1 = 0
    file2.close()
    # get the outline of the post
    logging.info("正在获取体育部文件的概要")
    text = ''
    flag = 0
    k = lastpart
    file = open('result.txt', 'r')
    for i in file.readlines():
        k += 1
        posts.append(Post())
        for j in i:
            if j != ' ':
                text += j
            if '<a' in text:
                flag = 1
                text = ''
            if flag == 1:
                if 'href=' in text:
                    text = ''
                    flag = 2
            if flag == 2:
                if j == '"':
                    flag = 3
                    text = ''
                    continue
            if flag == 3:
                if j == '"':
                    flag = 4
                    text = text.replace('"', "", 1)
                    print("https://pe2016.sspu.edu.cn" + text)
                    posts[k].setUrl("https://pe2016.sspu.edu.cn" + text)
                    text = ''
            if flag == 4:
                if 'target="_blank"' in text:
                    text = ''
                    flag = 5
            if flag == 5:
                if 'title=' in text:
                    text = ''
                    flag = 6
            if flag == 6:
                if j == '"':
                    flag = 7
                    text = ''
                    continue
            if flag == 7:
                if j == '"':
                    flag = 8
                    text = text.replace('"', "", 1)
                    print(text)
                    posts[k].setTitle(text)
                    print('------------------')
                    text = ''
            if flag == 8:
                flag = 0
                break
        file.close()
    logging.info("获取体育部文件的概要成功，正在获取体育部文件")
    for g in posts[lastpart + 1:]:
        url = g.url
        if url in oldPostList or g.title in oldPostList:
            continue
        try:
            if "files/" in url:
                g.setOutline("由于网页不支持打开，请到该站点查看")
                continue
            driver.get(url)
            outline = driver.find_element(By.XPATH, "//div[@class=\"wp_articlecontent\"]")
            outline = outline.text[:]
            g.setOutline(outline)
        except selenium.common.exceptions.NoSuchElementException:
            g.setOutline("由于网页不支持打开，请到该站点查看")
        g.setSource("体育部")


def getOfficialAccount():
    # get the information from WeChat Official Account
    logging.info("正在获取公众号的信息")
    driver.get("https://mp.weixin.qq.com")
    try:
        logging.info("正在登录公众号")
        login()
    finally:
        for i in websites:
            logging.info(f"正在获取{i}的文章")
            GetOfficialAccount(i, posts, len(posts) - 1, len(posts) - 1)
        # close the browser
        logging.info("正在关闭浏览器")
        for handle in driver.window_handles:
            driver.switch_to.window(handle)
            driver.close()
        driver.quit()


def get():
    # run the function to get the information from the school website
    getSchooljwc()
    getschoolpe()
    # run the function to get the information from the official account
    getOfficialAccount()


if __name__ == "__main__":
    get()
