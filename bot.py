import telebot
import threading
import api2ch
import random

bot = telebot.TeleBot('TOKEN')
api = api2ch.Api2ch()
boardsList = ['b', 'wp', 'zog']

def getPic(postUrl):
        valid, board, thread_id = api2ch.parse_url(postUrl)
        if not valid:
            print(404, 'Invalid URL')
            return ""
        try:
            thread = api.thread(board, thread_id)
        except:
            return ""
        text = ""
        while(True):
            post = thread.posts[random.randint(0, len(thread.posts)-1)]
            if post.files:
                text += (post.files[0].url() + "\n")
                return text
            else: continue

def sendPicsByTimer():
    recList = list()
    for i in range(0, len(boardsList)): recList.append(api.threads(boardsList[i]))
    num = random.randint(0, len(recList)-1)
    pic = getPic(recList[num].threads[random.randint(0, len(recList[num].threads)-1)].url(recList[num].board))
    try:
        bot.send_photo(-1001213878357, pic)
    except:
        print('404 пикча')
    timerTag = threading.Timer(300.0, sendPicsByTimer)
    timerTag.start()

sendPicsByTimer()
bot.polling(none_stop=True)