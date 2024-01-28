# - - coding:utf-8 - -
import platform
import sys
import time
import json
import requests
import logging

try:
    s = json.load(open("./data/settings/settings.json", "r", encoding="utf-8"))
except FileNotFoundError:
    s = json.load(open("../data/settings/settings.json", "r", encoding="utf-8"))
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename="log.txt", filemode='a+')  # 日志配置


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
    if isTest:
        logging.info("现在是测试模式")
        id = 19
    else:
        logging.info("现在是正式模式")
        id = 20
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
    else:
        print("Release failed!")
        print(responses.status_code)
        logging.error("Release" + post["title"] + " " + str(post["url"]) + " failed!")
        logging.error(str(responses.status_code) + " " + str(responses.content))
    logging.info("Release end!")


def releaseWechatAccountOverdueNotice():
    session = requests.Session()
    logging.info("Release start!")
    logging.info("正在尝试连接到服务器...")
    responses = session.get(s["url"])
    head = {
        "Accept": "application/vnd.api+json",
        "Content-Type": "application/vnd.api+json",
        "Authorization": "Token " + s["token"]
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
    responses = session.post(s["url"] + "/api/discussions", headers=head, json=data)
    if responses.status_code == 201:
        print("Release success!")
        logging.info("Release" + "微信公众号过期通知" + " success!")
    else:
        print("Release failed!")
        print(responses.status_code)
        logging.error("Release" + "微信公众号过期通知" + " failed!")
        logging.error(str(responses.status_code) + " " + str(responses.content))
    logging.info("Release end!")


if __name__ == "__main__":
    # file = open("result.md", "r")
    # outline = file.read()
    # file.close()
    content = "test"
    post = {
        "title": "test",
        "outline": "test",
        "url": "https://github.com/SSPUBot/SSPUBot"
    }
    release(s, post)
