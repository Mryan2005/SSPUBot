# import some modules
import os
import sys

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
            if checkThisPostIsNew(i, oldPostList) == 1:
                post = {
                    "title": i.title,
                    "outline": i.outline,
                    "url": i.url
                }
                res = r.release(s, post, True)
                flag = 1
            if i.url != "" and res == 1 and flag == 1:
                oldPosts.write(i.url + "\n")
            elif i.title != "" and res == 1 and flag == 1:
                oldPosts.write(i.title + '\n')
    except FileNotFoundError:
        oldPosts = open("./data/haveReleased.sspubot", "w", encoding="utf-8")
        for i in posts[:]:
            post = {
                "title": i.title,
                "outline": i.outline,
                "url": i.url
            }
            r.release(s, post, True)
            if i.url != "":
                oldPosts.write(i.url + "\n")
            else:
                oldPosts.write(i.title + '\n')
        oldPosts.close()


# run the bot if this file is the main file
if __name__ == "__main__":
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
