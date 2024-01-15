import platform
import sys
import time
import json
import requests

s = json.load(open("../settings/settings.json", "r", encoding="utf-8"))


def release(Url, token, title, content):
    session = requests.Session()
    responses = session.get(Url)
    head = {
        "Accept": "application/vnd.api+json",
        "Content-Type": "application/vnd.api+json",
        "Authorization": "Token " + token
    }
    data = {
        "data": {
            "type": "discussions",
            "attributes": {
                "title": title,
                "content": content
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
    responses = session.post(Url + "/api/discussions", headers=head, json=data)
    if responses.status_code == 201:
        print("Release success!")

if __name__ == "__main__":
    # file = open("result.md", "r")
    # content = file.read()
    # file.close()
    content = "test"
    release(s["url"], s["token"], "test", content)
