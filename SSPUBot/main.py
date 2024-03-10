# -*- coding: utf-8 -*-
# import some modules
import os
import sys

import jsonToPkl

try:
    from getInformation import getInformation as g
    from release import release as r
except ModuleNotFoundError:
    from SSPUBot.getInformation import getInformation as g
    from SSPUBot.release import release as r
finally:
    import datetime
    import json

s = json.load(open("data/settings/settings.json", "r", encoding="utf-8"))


# define the function to check if the post is new
def checkThisPostIsNew(each, post: dict):
    if str(each.url) + '\n' in post and str(each.url) != "":
        return 0
    elif str(each.title) + '\n' in post and str(each.url) == "":
        return 0
    else:
        return 1


# define the function to run the bot
def run():
    # define some values
    flag = 0
    res = 0
    g.get()
    posts = g.posts
    try:
        oldPosts = open("./data/haveReleased.sspubot", "r+", encoding="utf-8")
        oldPostList = oldPosts.readlines()
        for i in posts[:]:
            if checkThisPostIsNew(i, oldPostList):
                post = {
                    "title": i.title,
                    "outline": i.outline,
                    "url": i.url
                }
                res = r.release(s, post, s["isTest"])
                flag = 1
                if str(i.url) != "" and res == 1 and flag == 1:
                    oldPosts.write(str(i.url) + "\n")
                elif str(i.title) != "" and res == 1 and flag == 1:
                    oldPosts.write(str(i.title) + '\n')
    except FileNotFoundError:
        oldPosts = open("./data/haveReleased.sspubot", "w", encoding="utf-8")
        for i in posts[:]:
            post = {
                "title": i.title,
                "outline": i.outline,
                "url": i.url
            }
            if r.release(s, post, s["isTest"]):
                if str(i.url) != "":
                    oldPosts.write(str(i.url) + "\n")
                elif str(i, title):
                    oldPosts.write(str(i.title) + '\n')
        oldPosts.close()


# run the bot if this file is the main file
if __name__ == "__main__":
    if sys.argv[1] == "jtp":
        jsonToPkl.jsonToPkl()
        exit(0)
    if s["isLogin"]:
        run()
    else:
        try:
            if sys.argv[1] == "onDocker":
                os.system("pkill -f 'firefox'")
                os.system("pkill -f 'geckodriver'")
                os.system("pkill -f 'firefox-bin'")
        except IndexError:
            pass
