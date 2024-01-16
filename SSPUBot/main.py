# import some modules
try:
    from getInformation import getInformation as g
    from release import release as r
except ModuleNotFoundError:
    from SSPUBot.getInformation import getInformation as g
    from SSPUBot.release import release as r
finally:
    import datetime
    import json

s = json.load(open("settings/settings.json", "r", encoding="utf-8"))


# define the function to run the bot
def run():
    # define some values
    flag = 0
    count = 0
    noNotice = []
    g.get()
    file = open("result.md", "r")
    contents = file.readlines()
    file.close()
    # check the result.md
    for i in contents:
        if '## ' in i and flag == 0:
            flag = 1
            continue
        if flag == 1:
            if "\n" == i:
                flag = 2
                continue
        if flag == 2:
            if "## " in i:
                noNotice.append(1)
                flag = 3
            else:
                noNotice.append(0)
                flag = 0
            if "## " in i and contents.index(i) + 1 == len(contents):
                noNotice.append(1)
        if flag == 3:
            flag = 1
    for i in noNotice:
        if i == 1:
            count += 1
    if count != len(noNotice):
        file = open("result.md", "r")
        content = file.read()
        file.close()
        # get the date and time of releasing
        releasingTime = datetime.datetime.now()
        # release the result
        r.release(s["url"], s["username"], s["password"], releasingTime, content)


# run the bot if this file is the main file
if __name__ == "__main__":
    run()
