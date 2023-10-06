from apps.pyrogram_bot import pyrogram_bot
from apps.bot import myTeleBot

if __name__ == '__main__':
    print('Atempt to run telegrabber')
    pyrogram_bot.app.run()  # эта строка запустит все обработчики
    myTeleBot.bot.polling(none_stop=True)

