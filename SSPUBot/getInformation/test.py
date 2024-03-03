import json
import urllib.request

settings = json.load(open("../data/settings/settings.json", "r", encoding="utf-8"))


def getSchoolInformationFromSchoolWebsite():
    websites = settings['websites']
    for website in websites:
        text = ''
        flag = 0
        k = -1
        aWebsite = websites[f"{website}"]
        name = aWebsite['name']
        url = aWebsite['url']
        titleStartPoint = aWebsite['titleStartPoint']
        titleWriteStartPoint = aWebsite['titleWriteStartPoint']
        titleWriteEndPoint = aWebsite['titleWriteEndPoint']
        linkTagStartPoint = aWebsite['linkTagStartPoint']
        linkStartPoint = aWebsite['linkStartPoint']
        contentStartPoint = aWebsite['contentStartPoint']
        logging.info(f"正在获取{name}的信息")
        res = urllib.request.urlopen(url)
        htmlBytes = res.read()
        websiteResultList = open('website.html', 'wb')
        websiteResultList.write(htmlBytes)
        websiteResultList.close()
        HtmlFile = open('website.html', 'rb')
        result = open('result.txt', 'w', encoding='utf-8')
        texts = HtmlFile.readlines()
        HtmlFile.close()
        logging.info(f"正在处理{name}的信息")
        for i in texts:
            if titleStartPoint in i.decode('utf-8') and flag == 0:
                flag = 1
                print("find it")
                logging.info(f"找到{name}的靶子")
            if flag == 1:
                if titleWriteStartPoint in i.decode('utf-8'):
                    for j in i.decode('utf-8'):
                        if j != "\t" and flag1 == 0:
                            text = ''
                            j = ''
                            flag1 = 1
                        if flag1 == 1:
                            text += j
                            if titleWriteEndPoint in text:
                                result.write(text)
                                result.write("\n")
                                text = ''
                                flag1 = 0
            result.close()
            logging.info(f"正在获取{name}文件的链接")
            text = ''
            file = open('result.txt', 'r')
            for i in file.readlines():
                k += 1
                posts.append(Post())
                for j in i:
                    if j != ' ':
                        text += j
                    if linkTagStartPoint == text:
                        flag = 1
                        text = ''
                    if flag == 1:
                        if linkStartPoint == text:
                            text = ''
                            flag = 2
                    if flag == 2:
                        if j == '"' or j == "'":
                            text = ''
                            flag = 3
                    if flag == 3:
                        if j == '"' or j == "'":
                            flag = 4
                            text = text.replace("'", "", 1)
                            text = text.replace('"', "", 1)
                            if url not in text:
                                logging.info(f"{url}{text}")
                                posts[k].setUrl(f"{url}{text}")
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
                        if j == '"' or j == "'":
                            text = ''
                            flag = 7
                            continue
                    if flag == 7:
                        if j == '"' or j == "'":
                            text = text.replace("'", "", 1)
                            text = text.replace('"', "", 1)
                            posts[k].setTitle(text)
                            text = ''
                            flag = 8
                    if flag == 8:
                        flag = 0
                        break
            logging.info(f"获取{name}文件的链接成功")
            for g in posts:
                url_ = g.getUrl()
                try:
                    if "files/" in url:
                        g.setOutline("由于网页不支持打开，请到该站点查看")
                        continue
                    driver.get(url)
                    outline = driver.find_element(By.XPATH, contentStartPoint)
                    outline = outline.text[:]
                    g.setOutline(outline)
                except selenium.common.exceptions.NoSuchElementException:
                    g.setOutline("由于网页不支持打开，请到该站点查看")
                g.setSource(f"{name}")
