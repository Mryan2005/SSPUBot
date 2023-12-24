from getInformation import *
from release import *
from settings import *
def run():
    get()
    file = open("result.md", "r")
    content = file.read()
    file.close()
    release(user["url"], user["username"], user["password"], "test", content)
if __name__ == "__main__":
    run()