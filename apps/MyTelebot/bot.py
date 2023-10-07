import telebot
import os
from dotenv import load_dotenv
from apps.DB_actions import data_base

load_dotenv()
BOT_ID = os.getenv("BOT_ID")
bot = telebot.TeleBot(BOT_ID)


class TeleBot:
    bot = bot
    client_chat_id = 841210915
    @bot.message_handler(commands=['zachem'])
    def send_message(message):
        # получаем из базы пост по этому id

        print(message)





myTeleBot = TeleBot()
