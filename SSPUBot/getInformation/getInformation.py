# Function: get the information from the school website and the official account
# Path: SSPUBot/getInformation/getInformation.py
# Compare this snippet from SSPUBot/release/release.py:
import io
import pickle
import sys
import time
import urllib.request
import json

import selenium
import win32api
import win32con
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from seleniumwire import webdriver
from seleniumwire.webdriver import Firefox

try:
    settings = json.load(open("../settings/settings.json", "r", encoding="utf-8"))
except FileNotFoundError:
    print("settings.json not found")
    sys.exit(1)

# read the settings

# define the driver
ser = Service()
ser.path = 'C:\\Users\\A2564\\AppData\\Local\\Programs\\Python\\Python311\\geckodriver.exe'
firefox_options = Options()
# firefox_options.add_argument('--ignore-certificate-errors')
# firefox_options.add_argument('--proxy-server={0}'.format(proxy.proxy))
if sys.argv[0] == 'normal':
    firefox_options.add_argument("-headless")
elif sys.argv[0] == 'test':
    pass
driver: Firefox = webdriver.Firefox(options=firefox_options, service=ser)  # connect to the browser
driver.set_page_load_timeout(30)  # set the time to load the page
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')  # set the output encoding


# define the classes
# define the Error
class notLoginError(Exception):
    def __init__(self, ErrorInfo):
        super().__init__(self, ErrorInfo)
        self.errorinfo = ErrorInfo

    def __str__(self):
        return self.errorinfo


# define the post class
class Post(object):
    def __init__(self):
        self.outline = None
        self.file = None
        self.url = None
        self.title = None

    def setTitle(self, title):
        self.title = title

    def setUrl(self, url):
        self.url = url

    def setOutline(self, outline):
        self.outline = outline


# define the function to make error
def MakeError():
    raise notLoginError("如登")


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
    neededThings = ["name", "value", "domain", "path", "expiry", "secure", "httpOnly", "sameSite", "priority",
                    "sameParty", "sourceScheme", "sourcePort", "sourcePriority", "isSameSite", "isSameParty",
                    "isSecure",
                    "isHttpOnly", "isHostOnly", "isSession", "isPersistent", "isExpired", "isSecureContext",
                    "isFirstPartyOnly", "sameSiteStatus", "samePartyStatus", "priorityValue", "sourcePriorityValue",
                    "sameSiteValue", "samePartyValue", "priorityValue", "sourcePriorityValue", "sameSiteValue",
                    "samePartyValue", "domain"]
    try:
        # login with cookies
        cookies = pickle.load(open("taobao_cookies.pkl", "rb"))
        for cookie in cookies:
            if isinstance(cookie.get('expiry'), float):
                cookie['expiry'] = int(cookie['expiry'])
            driver.add_cookie(cookie)
        driver.refresh()
        writeafile = driver.find_elements(By.XPATH, "//div[@class=\"new-creation__menu-title\"]")
        if len(writeafile) == 0:
            MakeError()
    except FileNotFoundError:
        # login with username and password
        LoginTag = driver.find_element(By.XPATH, "//a[@class=\"login__type__container__select-type\"]")
        LoginTag.click()
        UserNameTag = driver.find_element(By.XPATH, "//input[@name=\"account\"]")
        UserNameTag.send_keys(settings["weixinUsername"])
        PasswordTag = driver.find_element(By.XPATH, "//input[@name=\"password\"]")
        PasswordTag.send_keys(settings["weixinPassword"])
        LoginTag = driver.find_element(By.XPATH, "//a[@class=\"btn_login\"]")
        LoginTag.click()
        time.sleep(60)
        cookie = driver.get_cookies()
        pickle.dump(cookie, open('taobao_cookies.pkl', 'wb'))
        driver.refresh()
        writeafile = driver.find_elements(By.XPATH, "//div[@class=\"new-creation__menu-title\"]")
        if len(writeafile) == 0:
            MakeError()
        cookies = pickle.load(open("taobao_cookies.pkl", "rb"))
        for cookie in cookies:
            if isinstance(cookie.get('expiry'), float):
                cookie['expiry'] = int(cookie['expiry'])
            driver.add_cookie(cookie)
    except notLoginError or IndexError:
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
        win32api.MessageBox(0, "请扫码登录", "提醒", win32con.MB_OK)
        time.sleep(60)
        cookie = driver.get_cookies()
        pickle.dump(cookie, open('taobao_cookies.pkl', 'wb'))
        driver.refresh()
        cookies = pickle.load(open("taobao_cookies.pkl", "rb"))
        for cookie in cookies:
            if isinstance(cookie.get('expiry'), float):
                cookie['expiry'] = int(cookie['expiry'])
            driver.add_cookie(cookie)


# define the function to get the official account information
def GetOfficialAccount(accountName, posts, k, lastpart):
    time.sleep(3)
    # define some values
    writeafile = []
    openingTag = []

    try:
        writeafile = driver.find_elements(By.XPATH, "//div[@class=\"new-creation__menu-title\"]")
    except selenium.common.exceptions.NoSuchElementException:
        time.sleep(30)
        writeafile = driver.find_elements(By.XPATH, "//div[@class=\"new-creation__menu-title\"]")
    finally:
        writeafile[0].click()
    time.sleep(5)
    windows = driver.window_handles
    driver.switch_to.window(windows[-1])
    time.sleep(3)

    try:
        openingTag = driver.find_element(By.XPATH, "//li[@id=\"js_editor_insertlink\"]")
    except selenium.common.exceptions.NoSuchElementException:
        time.sleep(30)
        openingTag = driver.find_element(By.XPATH, "//li[@id=\"js_editor_insertlink\"]")
    finally:
        openingTag.click()
        time.sleep(3)

    del driver.requests

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
    requestList = driver.requests
    url = ""
    for i in requestList:
        if "mp.weixin.qq.com" in i.url:
            if "cgi-bin/appmsgpublish?sub=list&search_field=null" in i.url:
                if not ('&query=&fakeid=&' in i.url):
                    url = i.url
                    break
    driver.get(url)
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
    # get the outline of the post
    file3 = open("./result.md", "a")
    for g in posts[lastpart + 1:]:
        try:
            url = g.url
        except AttributeError:
            g.setOutline("由于网页不支持打开，请到该站点查看")
            continue
        try:
            time.sleep(3)
            try:
                driver.get(url)
            except selenium.common.exceptions.InvalidArgumentException:
                g.setOutline("由于网页不支持打开，请到该站点查看")
            try:
                time.sleep(3)
                outlines = driver.find_elements(By.XPATH, "//section")
            except selenium.common.exceptions.NoSuchElementException:
                time.sleep(30)
                outlines = driver.find_elements(By.XPATH, "//section")
            try:
                outline = outlines[0].text[:200]
                g.setOutline(outline)
            except selenium.common.exceptions.StaleElementReferenceException:
                g.setOutline("由于网页不支持打开，请到该站点查看")
            except IndexError:
                g.setOutline("可能内容被删除了，或者这是张图片")
        except selenium.common.exceptions.NoSuchElementException:
            g.setOutline("由于网页不支持打开，请到该站点查看")
    # write the account name to the file
    file3.write("## " + accountName + "\n\n")
    for g in posts[lastpart + 1:]:
        outline = g.outline
        outline = outline.replace("\n", " ")
        outline = outline.replace(" ", " ")
        outline = outline.replace("²", "平方")
        g.setOutline(outline)
    # close the page, select the first page and refresh the page.
    driver.close()
    windows = driver.window_handles
    driver.switch_to.window(windows[0])
    driver.refresh()


# define the function to get the information from the school website

def getSchooljwc():
    text = ''
    flag = 0
    flag1 = 0
    k = -1
    # get the information from the school website which is "jwc.sspu.edu.cn"
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
    for g in posts:
        url = g.url
        try:
            driver.get(url)
            outline = driver.find_element(By.XPATH, "//div[@class=\"WordSection1\"]")
            outline = outline.text[:200]
            g.setOutline(outline)
        except selenium.common.exceptions.NoSuchElementException:
            g.setOutline("由于网页不支持打开，请到该站点查看")
    # get the outline of the post ---- end
    # check the posts, if url in havereleased.log, then delete it ---- start
    try:
        file4 = open("./havereleased.log", "r+")
    except FileNotFoundError:
        file4 = open("./havereleased.log", "w+")
    havereleased = file4.readlines()
    file4.close()
    file4 = open("./havereleased.log", "a")
    flag = 1
    while flag == 1:
        flag = 0
        for o in posts:
            try:
                if o.url + "\n" in havereleased:
                    posts.remove(o)
                    flag = 1
            except AttributeError:
                if o.title + "\n" in havereleased:
                    posts.remove(o)
                    flag = 1
    for o in posts:
        try:
            file4.write(o.url + "\n")
        except AttributeError:
            file4.write(o.title + "\n")
    file4.close()
    # check the posts, if url in havereleased.log, then delete it ---- end
    # write the posts to the file ---- start
    file3 = open("./result.md", "w")
    file3.write("## 教务处通知\n\n")
    for o in posts:
        file3.write("[")
        file3.write(o.title)
        file3.write("](")
        file3.write(o.url)
        file3.write(")  \n")
        file3.write(o.outline + "……")
        file3.write("\n\n")
    file3.close()
    # write the posts to the file ---- end


def getschoolpe():
    # get the information from the school website which is "pe2016.sspu.edu.cn"
    # define some values ---- start
    lastpart = len(posts) - 1
    text = ''
    flag = 0
    flag1 = 0
    # define some values ---- end
    # get the title and the url of the post
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
    for g in posts[lastpart + 1:]:
        url = g.url
        try:
            if "files/" in url:
                g.setOutline("由于网页不支持打开，请到该站点查看")
                continue
            driver.get(url)
            outline = driver.find_element(By.XPATH, "//div[@class=\"wp_articlecontent\"]")
            outline = outline.text[:200]
            g.setOutline(outline)
        except selenium.common.exceptions.NoSuchElementException:
            g.setOutline("由于网页不支持打开，请到该站点查看")
    file3 = open("./result.md", "a")
    file3.write("## 体育部通知\n\n")
    # check the posts, if url in havereleased.log, then delete it
    file4 = open("./havereleased.log", "r")
    havereleased = file4.readlines()
    file4.close()
    file4 = open("./havereleased.log", "a")
    flag = 1
    while flag == 1:
        flag = 0
        for o in posts:
            try:
                if o.url + "\n" in havereleased:
                    posts.remove(o)
                    flag = 1
            except AttributeError:
                if o.title + "\n" in havereleased:
                    posts.remove(o)
                    flag = 1
    # write the posts to the file
    for o in posts:
        file3.write("[")
        file3.write(o.title)
        file3.write("](")
        file3.write(o.url)
        try:
            file4.write(o.url + "\n")
        except AttributeError:
            file4.write(o.title + "\n")
        file3.write(")  \n")
        file3.write(o.outline + "……")
        file3.write("\n\n")
    file3.close()
    file4.close()


def getOfficialAccount():
    # get the information from WeChat Official Account
    driver.get("https://mp.weixin.qq.com")
    try:
        login()
    finally:
        GetOfficialAccount("青春二工大", posts, len(posts) - 1, len(posts) - 1)
        GetOfficialAccount("上海第二工业大学学生事务中心", posts, len(posts) - 1, len(posts) - 1)
        # check the posts, if url in havereleased.log, then delete it
        try:
            file4 = open("./havereleased.log", "r+", encoding="gb2312")
        except FileNotFoundError:
            file4 = open("./havereleased.log", "w+", encoding="gb2312")
        havereleased = file4.readlines()
        file4.close()
        file4 = open("./havereleased.log", "a+")
        flag = 1
        while flag == 1:
            flag = 0
            for o in posts:
                try:
                    if o.url + "\n" in havereleased:
                        posts.remove(o)
                        flag = 1
                except AttributeError:
                    if o.title + "\n" in havereleased:
                        posts.remove(o)
                        flag = 1
                except TypeError:
                    if o.title + "\n" in havereleased:
                        posts.remove(o)
                        flag = 1
        for o in posts:
            try:
                file4.write(o.url + "\n")
            except AttributeError:
                file4.write(o.title + "\n")
            except TypeError:
                file4.write(o.title + "\n")
        file4.close()
        # write the posts to the file
        file3 = open("./result.md", "a")
        for o in posts:
            file3.write("[")
            try:
                file3.write(o.title)
                file3.write("](")
            except UnicodeEncodeError:
                text1 = ""
                for i in o.title:
                    if is_word_which_i_need(i):
                        text1 += i
                file3.write(text1)
                file3.write("](")
            try:
                file3.write(o.url)
                file3.write(")  \n")
            except AttributeError:
                file3.write(")  \n")
            except TypeError:
                file3.write(")  \n")
            try:
                file3.write(o.outline + "……")
            except UnicodeEncodeError:
                text = ''
                for i in o.outline:
                    if is_word_which_i_need(i):
                        text += i
                file3.write(text + "……")
            file3.write("\n\n")
        # write the posts to the file ---- end
        file3.close()
        # close the browser
        driver.quit()


def get():
    # run the function to get the information from the school website
    getSchooljwc()
    getschoolpe()
    # run the function to get the information from the official account
    getOfficialAccount()


if __name__ == "__main__":
    get()
