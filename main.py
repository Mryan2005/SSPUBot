import io
import requests
import os
import sys
import time
import urllib.request
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
res=urllib.request.urlopen('https://jwc.sspu.edu.cn/897/list.htm')
htmlBytes=res.read()
filr = open('website.html','wb')
filr.write(htmlBytes)
filr.close()
filr = open('website.html','rb')
filr.close()
file = open('website.html','rb')
file2 = open('result.txt','w')
texts = file.readlines()
file.close()
text = ''
flag = 0
flag1 = 0
import unicodedata
def is_word_which_i_need(chars):
    for i in chars:
        if '\u4e00' <= i <= '\u9fff':
            return True
        elif '0' <= i <= '9':
            return True
        elif '-' == i:
            return True
        else:
            return False
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
count = 0
for g in posts:
    url = g.url
    res=urllib.request.urlopen(url)
    htmlBytes=res.read()
    filr = open('website.html','wb')
    filr.write(htmlBytes)
    filr.close()
    filr = open('website.html','rb')
    filr.close()
    file = open('website.html','rb')
    texts = file.readlines()
    file.close()
    text = ''
    flag = 0
    flag1 = 0
    result = ''
    post1 = []
    doNotRecord = -1
    for j in texts:
        for o in j.decode("utf8"):
            if(o != ' '):
                text += o
            if('<p class="arti_metas">' in text):
                flag = 1
                text = ''
            if(o == '<'):
                if(not doNotRecord):
                     if('</span>' in text and not doNotRecord):
                        for a in text:
                            if(is_word_which_i_need(a)):
                                result += a
                                if(result == '宋体'):
                                    result = ""
                        post1.append(result)
                        text = ''
                        result = ''
                else:
                    doNotRecord = 1
            elif(o == '>'):
                doNotRecord = 0
                if(not is_word_which_i_need(text)):
                    text = ''
    posts[count].setOutline(post1[0])
    count += 1
count -= 1
res=urllib.request.urlopen('https://jwc.sspu.edu.cn/897/list.htm')
htmlBytes=res.read()
filr = open('website.html','wb')
filr.write(htmlBytes)
filr.close()
filr = open('website.html','rb')
filr.close()
file = open('website.html','rb')
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
text = ''
flag = 0
file = open('result.txt','r')
file1 = open("result.md",'w')
file1.write("## 教务处通知\n")
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
for g in posts:
    url = g.url
    res=urllib.request.urlopen(url)
    htmlBytes=res.read()
    filr = open('website.html','wb')
    filr.write(htmlBytes)
    filr.close()
    filr = open('website.html','rb')
    filr.close()
    file = open('website.html','rb')
    texts = file.readlines()
    file.close()
    text = ''
    flag = 0
    flag1 = 0
    result = ''
    post1 = []
    doNotRecord = -1
    for j in texts:
        for k in j.decode("utf8"):
            if(k != ' '):
                text += k
            if('<p class="arti_metas">' in text):
                flag = 1
                text = ''
            if(k == '<'):
                if(not doNotRecord):
                     if('</span>' in text and not doNotRecord):
                        for a in text:
                            if(is_word_which_i_need(a)):
                                result += a
                                if(result == '宋体'):
                                    result = ""
                        post1.append(result)
                        text = ''
                        result = ''
                else:
                    doNotRecord = 1
            elif(k == '>'):
                doNotRecord = 0
                if(not is_word_which_i_need(text)):
                    text = ''
    posts[count].setOutline(post1[0])
    count += 1
    if(count == len(posts)):
        break
class PostGot(object):
    def setTitle(self,title):
        self.title = title
    def setUrl(self,url):
        self.url = url
    def setOutline(self,outline):
        self.outline = outline
postsGot = []
try:
    file2 = open("releaseedPost.log",'r')
    log = file2.readlines()
    c = 1
    for i in log:
        if(c == 1):
            postsGot.append(PostGot())
            postsGot[len(postsGot)-1].setTitle(i)
            c += 1
        elif(c == 2):
            postsGot[len(postsGot)-1].setUrl(i)
            c += 1
        elif(c == 3):
            postsGot[len(postsGot)-1].setOutline(i)
            c = 1
    file2.close()
except FileNotFoundError:
    file2 = open("releaseedPost.log",'w')
    log = []
    file2.close()
finally:
    file2 = open("releaseedPost.log",'w')
    for i in posts:
        file2.write(i.title)
        file2.write('\n')
        file2.write(i.url)
        file2.write('\n')
        file2.write(i.outline)
        file2.write('\n')
    file2.close()
# save to md
have = 0
for i in posts:
    if(i.title+'\n' in log):
        continue
    file1.write("[")
    file1.write(i.title)
    file1.write("](")
    file1.write(i.url)
    file1.write(")")
    file1.write('\n')
    file1.write(i.outline[:200])
    file1.write('\n')
    file1.write('\n')
    have = 1
if(not have):
    file1.write("老兄，截止到现在，教务处没有发布新的通知，你可以通过搜索栏查看往期通知\n")
file1.close()
