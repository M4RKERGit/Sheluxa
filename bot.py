import telebot
import threading
import api2ch
import random
import re
import time
import os, sys

bot = telebot.TeleBot('TOKEN')
api = api2ch.Api2ch()
tagsList = ['засмеялся', 'webm', 'обосрался', 'тредшот', 'субкот']
urlList = list()

def verifyPic(url):
    global urlList
    print(len(urlList))
    if not url in urlList:
        if len(urlList) >= 2000:  urlList.pop(0)
        urlList.append(url)
        return True
    else:
        return False

def getPic(num, mode):
    thread = api.thread(mode, num)
    c = 0
    buf = ''
    while(True):
        post = thread.posts[random.randint(0, len(thread.posts)-1)]
        if post.files:
            buf = post.files[0].url()
            if verifyPic(buf): break
            else:
                c += 1
                if (c > 20): os.execl(sys.executable, sys.executable, *sys.argv)
                continue
    return (buf + "\n")

def sendPicsByTimer():
    c = 0
    if time.localtime().tm_hour <= 6 or time.localtime().tm_hour >= 22:    postingMode = 'wp'
    else: postingMode = 'b'
    recList = api.threads(postingMode)
    while(True):
        thread = recList.threads[random.randint(0, len(recList.threads)-1)]
        if postingMode == 'wp': break
        if c >= len(recList.threads): break
        c += 1
        for i in range(0, len(tagsList)):
            if re.search(tagsList[i], thread.body):    break
    pic = getPic(thread.num, postingMode)
    try:
        if postingMode == 'wp':
            bot.send_message(CHAT, pic)
        else:   bot.send_photo(CHAT, pic)
    except: 
        print('404 пикча')
        sendPicsByTimer()
        return
    timerTag = threading.Timer(300.0, sendPicsByTimer)
    timerTag.start()

sendPicsByTimer()