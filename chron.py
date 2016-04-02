import datetime as dt
import telebot
import time

bot = telebot.TeleBot ('214286801:AAGL7tBjGjdfW2hHCc_yo_2w4KvblXPgZow')

def iscurrent (line):
    l = line.split (' ')
    now = dt.datetime.now ()
    iso = now.isocalendar ()
    weekN = iso[1] % now.month
    now = [weekN, now.isoweekday (), now.hour, now.minute]
    print ('now = ', now)
    flag = True
    for i in range (4):
        print (l[i], now[i])
        if l[i] != '*' and l[i] != str (now[i]):
            flag = False
    
    return flag




def readDb():
    with open ('chron.db', 'r') as fp:
        line = fp.readline ().rstrip ('\n')
        while line:
            line = line.split (' REMOVE:')[0]
            line = line.split (' TEXT:')
            msg = line[-1].split (' ID:')
            msgId = msg.pop ()
            msg = str (msg[0])
            line = line[0]
            print (line, msg, msgId)
            if iscurrent (line):
                print ('sending')
                bot.send_message (msgId, msg) 
            line = fp.readline ().rstrip ('\n')

if __name__ == '__main__':
    while True:
        readDb ()
        time.sleep (60)
