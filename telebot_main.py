from apps.MyTelebot.bot import myTeleBot

if __name__ == '__main__':
    print('Atempt to run TeleBot')
    myTeleBot.bot.polling(none_stop=True)

