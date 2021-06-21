import telebot
import threading
import api2ch
import random
import re
import time

bot = telebot.TeleBot('TOKEN')
api = api2ch.Api2ch()
tagsList = ['засмеялся', 'webm', 'обосрался', 'тредшот']
urlList = list()

def verifyPic(url):
    for i in range(0, len(urlList)):
        if url == urlList[i]:   return False
    if len(urlList) >= 50:  urlList.pop(0)
    urlList.append(url)
    return True

def getPic(num, mode):
    thread = api.thread(mode, num)
    while(True):
        post = thread.posts[random.randint(0, len(thread.posts)-1)]
        if post.files:
            while(True):
                buf = post.files[0].url()
                if verifyPic(buf): break
            return (buf + "\n")
        else: continue

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
            bot.send_message(-1001213878357, pic)
        else:   bot.send_photo(-1001213878357, pic)
    except: print('404 пикча')
    timerTag = threading.Timer(300.0, sendPicsByTimer)
    timerTag.start()

sendPicsByTimer()