import io
import requests
import os
import sys
import urllib.request
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
res=urllib.request.urlopen('https://jwc.sspu.edu.cn/897/list.htm')
htmlBytes=res.read()
filr = open('baidu.html','wb')
filr.write(htmlBytes)
filr.close()
filr = open('baidu.html','rb')
filr.close()
file = open('baidu.html','rb')
file2 = open('result.txt','w')
texts = file.readlines()
file.close()
text = ''
flag = 0
flag1 = 0
for i in texts:
    if('<ul class="news_list list2">' in i.decode("utf8") and flag == 0):
        flag = 1
        print("find")
    if(flag == 1):
        if('<span class="news_title">' in i.decode("utf8")):
            for j in i.decode("utf8"):
                if(j != '\t' and flag1 == 0):
                    text += j
                if('<span class="news_title">' in text and flag1 == 0):
                    text = ''
                    j = ''
                    flag1 = 1
                if(flag1 == 1):
                    if(j != '\n' and j != '\t'):
                        text += j
                        if('</span>' in text):
                            #print(text)
                            file2.write(text)
                            file2.write('\n')
                            text = ''
                            flag1 = 0                    
file2.close()
class Post(object):
    def setTitle(self,title):
        self.title = title
    def setUrl(self,url):
        self.url = url
    def setOutline(self,outline):
        self.outline = outline
posts = []
text = ''
flag = 0
k = -1
file = open('result.txt','r')
file1 = open("result.md",'w')
for i in file.readlines():
    k += 1
    posts.append(Post())
    for j in i:
        if(j != ' '):
            text += j
        if('<a' == text):
            flag = 1
            text = ''
        if(flag == 1):
            if('href=' == text):
                text = ''
                flag = 2
        if(flag == 2):
            if(j == "'"):
                flag = 3
                text = ''
                continue
        if(flag == 3):
            if(j == "'"):
                flag = 4
                text = text.replace("'","",1)
                print("https://jwc.sspu.edu.cn" + text)
                posts[k].setUrl("https://jwc.sspu.edu.cn" + text)
                print('------------------')
                text = ''
        if(flag == 4):
            if("target='_blank'" == text):
                text = ''
                flag = 5
        if(flag == 5):
            if('title=' == text):
                text = ''
                flag = 6
        if(flag == 6):
            if(j == "'"):
                flag = 7
                text = ''
                continue
        if(flag == 7):
            if(j == "'"):
                flag = 8
                text = text.replace("'","",1)
                print(text)
                posts[k].setTitle(text)
                print('------------------')
                text = ''
        if(flag == 8):
            flag = 0
            break
# get the outline of the post
"""
for i in posts:
    url = i.url
    res=urllib.request.urlopen(url)
    htmlBytes=res.read()
    filr = open('baidu.html','wb')
    filr.write(htmlBytes)
    filr.close()
    filr = open('baidu.html','rb')
    filr.close()
    file = open('baidu.html','rb')
    texts = file.readlines()
    file.close()
    text = ''
    flag = 0
    flag1 = 0
"""
# save to md
for i in posts:
    file1.write("[")
    file1.write(i.title)
    file1.write("](")
    file1.write(i.url)
    file1.write(")")
    file1.write('{target="_blank"}')
    file1.write('\n')
    file1.write('\n')
file1.close()