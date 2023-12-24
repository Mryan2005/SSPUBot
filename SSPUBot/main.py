try:
    from getInformation import getInformation as g
    from release import release as r
    from settings import settings as s
except ModuleNotFoundError:
    from SSPUBot.getInformation import getInformation as g
    from SSPUBot.release import release as r
    from SSPUBot.settings import settings as s
def run():
    g.get()
    file = open("result.md", "r")
    content = file.read()
    file.close()
    r.release(s.user["url"], s.user["username"], s.user["password"], "test", content)
if __name__ == "__main__":
    run()