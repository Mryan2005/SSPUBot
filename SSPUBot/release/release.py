# - - coding:utf-8 - -
import platform
import sys
import time
import json
import requests

s = json.load(open("./settings/settings.json", "r", encoding="utf-8"))


def release(Url, token, title, outline, url, isTest):
    session = requests.Session()
    responses = session.get(Url)
    head = {
        "Accept": "application/vnd.api+json",
        "Content-Type": "application/vnd.api+json",
        "Authorization": "Token " + token
    }
    if isTest:
        id = 19
    else:
        id = 20
    data = {
        "data": {
            "type": "discussions",
            "attributes": {
                "title": title,
                "content": outline + "  \n[ 前往官网 ](" + url + ")"
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


if __name__ == "__main__":
    # file = open("result.md", "r")
    # outline = file.read()
    # file.close()
    content = "test"
    release(s["url"], s["token"], "test", content, "github.com/SSPUBot/SSPUBot", True)
