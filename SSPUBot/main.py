# import some modules
import time

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


# define the function to run the bot
def run():
    # define some values
    flag = 0
    count = 0
    noNotice = []
    g.get()
    posts = g.posts
    try:
        oldPosts = open("./data/haveReleased.sspubot", "r+", encoding="utf-8")
        oldPostList = oldPosts.readlines()
    except FileNotFoundError:
        oldPosts = open("./data/haveReleased.sspubot", "w", encoding="utf-8")
        oldPostList = []
    for i in posts[:]:
        if str(i.url) + "\n" in oldPostList and str(i.title) + '\n' in oldPostList:
            continue
        r.release(s["url"], s["token"], i.title, i.outline, i.url, True)
        if i.url != "":
            oldPosts.write(i.url + "\n")
        else:
            oldPosts.write(i.title + '\n')
    oldPosts.close()


# run the bot if this file is the main file
if __name__ == "__main__":
    while True:
        print("Start at " + str(datetime.datetime.now()))
        run()
        time.sleep(1 * 60 * 30)
