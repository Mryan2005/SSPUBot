# - - coding:utf-8 - -
import json
import logging

import requests


class goto(Exception):
    pass


def goto1():
    raise goto
    
def checkAndTagIt(tagsKeywords, theContectOfPost):
    for i in tagsKeywords["information"]:
        if i in theContectOfPost:
            id = 22
    for i in tagsKeywords["outsideClass"]:
        if i in theContectOfPost:
            id = 23
    return id


try:
    s = json.load(open("./data/settings/settings.json", "r", encoding="utf-8"))
except FileNotFoundError:
    s = json.load(open("../data/settings/settings.json", "r", encoding="utf-8"))
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename="./data/log.txt", filemode='a+')  # 日志配置


# setting { url, token }
# post { title, outline, url }
def release(setting: dict, post: dict, isTest: bool = True):
    session = requests.Session()
    logging.info("Release start!")
    logging.info("正在尝试连接到服务器...")
    responses = session.get(setting["url"])
    head = {
        "Accept": "application/vnd.api+json",
        "Content-Type": "application/vnd.api+json",
        "Authorization": "Token " + setting["token"]
    }
    if isTest == True:
        logging.info("现在是测试模式")
        id = 19
        data = {
            "data": {
                "type": "discussions",
                "attributes": {
                    "title": post["title"],
                    "content": post["outline"] + "  \n[ 前往官网 ](" + str(post["url"]) + ")"
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
        responses = session.post(setting["url"] + "/api/discussions", headers=head, json=data)
        if responses.status_code == 201:
            print("Release success!")
            logging.info("Release" + post["title"] + " " + str(post["url"]) + " success!")
            res = True
        else:
            print("Release failed!")
            print(responses.status_code)
            logging.error("Release" + post["title"] + " " + str(post["url"]) + " failed!")
            logging.error(str(responses.status_code) + " " + str(responses.content))
            res = false
        logging.info("Release end!")
    elif isTest == False:
        logging.info("现在是正式模式")
        i = setting["tags"]
        try:
            for j in i["information"]:
                if j in post["title"]:
                    data = {
                        "data": {
                            "type": "discussions",
                            "attributes": {
                                "title": post["title"],
                                "content": post["outline"] + "  \n[ 前往官网 ](" + str(post["url"]) + ")"
                            },
                            "relationships": {
                                "tags": {
                                    "data": [
                                        {
                                            "type": "tags",
                                            "id": "20"
                                        },
                                        {
                                            "type": "tags",
                                            "id": "23"
                                        }
                                    ]
                                }
                            }
                        }
                    }
                    goto1()
            for j in i["outsideClass"]:
                if j in post["title"]:
                    data = {
                        "data": {
                            "type": "discussions",
                            "attributes": {
                                "title": post["title"],
                                "content": post["outline"] + "  \n[ 前往官网 ](" + str(post["url"]) + ")"
                            },
                            "relationships": {
                                "tags": {
                                    "data": [
                                        {
                                            "type": "tags",
                                            "id": "20"
                                        },
                                        {
                                            "type": "tags",
                                            "id": "22"
                                        }
                                    ]
                                }
                            }
                        }
                    }
                    goto1()
            data = {
                "data": {
                    "type": "discussions",
                    "attributes": {
                        "title": post["title"],
                        "content": post["outline"] + "  \n[ 前往官网 ](" + str(post["url"]) + ")"
                    },
                    "relationships": {
                        "tags": {
                            "data": [
                                {
                                    "type": "tags",
                                    "id": "20"
                                }
                            ]
                        }
                    }
                }
            }
        except goto:
            pass
        responses = session.post(setting["url"] + "/api/discussions", headers=head, json=data)
        if responses.status_code == 201:
            print("Release success!")
            logging.info("Release" + post["title"] + " " + str(post["url"]) + " success!")
            res = True
        else:
            print("Release failed!")
            print(responses.status_code)
            logging.error("Release" + post["title"] + " " + str(post["url"]) + " failed!")
            logging.error(str(responses.status_code) + " " + str(responses.content))
            res = false
        logging.info("Release end!")
    elif isTest is None:
        res = True
        pass
    return res


if __name__ == "__main__":
    # file = open("result.md", "r")
    # outline = file.read()
    # file.close()
    content = "test"
    post = {
        "title": "test",
        "outline": "test",
        "url": "https://github.com/Mryan2005/SSPUBot"
    }
    release(s, post)
