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
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename="log.txt", filemode='a+')  # 日志配置


def release(Url, token, title, outline, url, isTest):
    session = requests.Session()
    logging.info("Release start!")
    logging.info("正在尝试连接到服务器...")
    responses = session.get(Url)
    head = {
        "Accept": "application/vnd.api+json",
        "Content-Type": "application/vnd.api+json",
        "Authorization": "Token " + token
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
                "title": title,
                "content": outline + "  \n[ 前往官网 ](" + str(url) + ")"
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
    responses = session.post(Url + "/api/discussions", headers=head, json=data)
    if responses.status_code == 201:
        print("Release success!")
        logging.info("Release"+ title + " " + str(url) + " success!")
    else:
        print("Release failed!")
        logging.error("Release"+ title + " " + str(url) + " failed!")
    logging.info("Release end!")


if __name__ == "__main__":
    # file = open("result.md", "r")
    # outline = file.read()
    # file.close()
    content = "test"
    release(s["url"], s["token"], "test", content, "github.com/SSPUBot/SSPUBot", True)
