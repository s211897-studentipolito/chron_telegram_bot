import telebot, subprocess
bot = telebot.TeleBot ('214286801:AAGL7tBjGjdfW2hHCc_yo_2w4KvblXPgZow')

@bot.message_handler (commands=['start', 'help'])
def send_welcome (message):
    bot.reply_to (message, 'this is a chron bot\n\
options are: every month, week, day, hour\n\
to schedule your action insert numbers or * for any.\n\
\nexample:\n\
Run once a month, second week,  monday, 10:40 -> "2 1 10 40",\n\n\
run every week, on thursday, 11:20 -> "* 4 11 20",\n\n\
run once a day, 16:35 -> "* * 16 35"\n\n\
run every hour, at 20 min after the beginning of the hour -> "* * * 20"\n\n\
run every minute -> "* * * *"\n\ninsert the text after a COMMA\n\nsend /remove ID to delete a scheduled action\n')

def check_validity (time):
    print (time)
    time = time.split (' ')
    for i in range (4):
        print (time[i])
        if time[i] != '*' and not time[i].isdigit ():
            return False
    print ('returning true')
    return True

@bot.message_handler (commands=['remove'])
def remove (message):
    removalId = message.text.split ('/remove ')[1].rstrip ('\n')
    with open ('chron.db', 'r') as fp:
        with open ('tmp.db', 'w') as tmp:
            line = fp.readline ()
            while line:
                currentId = line.split ('REMOVE:')[-1].rstrip ('\n')

                chatId = line.split ('ID:')[1]
                chatId = chatId.split (' REMOVE:')
                chatId = chatId[0]

                print (chatId)
                if removalId != currentId or int (chatId) != message.chat.id:
                    print ('writing')
                    tmp.write (line)
                line = fp.readline ()
    subprocess.call (['mv', 'tmp.db', 'chron.db'])

@bot.message_handler (func=lambda m: True)
def schedule (message):
    try:
        text = message.text
        text = text.split (',', 1)
        time = text.pop (0)
        print (time, text)
        if not check_validity (time):
            raise ValueError

        if time[-1] == ' ':
            time = time[:-1] 
        with open ('lastid', 'r') as fp:
            lastId = fp.readline ()
            print (lastId)
        lastId = int (lastId) + 1
        with open ('lastid', 'w') as fp:
            fp.write (str (lastId))

        with open ('chron.db', 'a') as fp:
            fp.write (time + ' TEXT: ' + text[0] + ' ID:' + str (message.chat.id) + ' REMOVE:' + str (lastId) + '\n')

        bot.send_message (message.chat.id, 'message scheduled, removal id is: ' + str( lastId))

    except:
        bot.reply_to (message, 'wrong format')



if __name__ == '__main__':
    while True:
        try:
            bot.polling
        except:
            pass
