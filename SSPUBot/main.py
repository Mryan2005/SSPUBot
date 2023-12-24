try:
    from getInformation import getInformation as g
    from release import release as r
    from settings import settings as s
except ModuleNotFoundError:
    from SSPUBot.getInformation import getInformation as g
    from SSPUBot.release import release as r
    from SSPUBot.settings import settings as s
def run():
    flag = 0
    count = 0
    noNotice = [0, 0, 0]
    g.get()
    file = open("result.md", "r")
    contents = file.readlines()
    file.close()
    for i in contents:
        if("## 教务处通知" == i and flag == 0):
            flag = 1
        if(flag == 1):
            if("\n" == i):
                flag = 2
        if(flag == 2):
            if("## 体育部通知" == i):
                noNotice[0] = 1
            flag = 3
        if(flag == 3):
            if("\n" == i):
                flag = 4
        if(flag == 4):
            if("## 青春二工大" == i):
                noNotice[1] = 1
            flag = 5
        if(flag == 5):
            if("\n" == i):
                flag = 6
        if(flag == 6):
            if("\n" == i):
                noNotice[2] = 1
                break
    for i in noNotice:
        if(i == 1):
            count += 1
    if(count != 3):
        file = open("result.md", "r")
        content = file.read()
        file.close()
        r.release(s.user["url"], s.user["username"], s.user["password"], "test", content)
if __name__ == "__main__":
    run()