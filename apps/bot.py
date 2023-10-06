import telebot
import os
from dotenv import load_dotenv
load_dotenv()

BOT_ID = os.getenv("BOT_ID")

bot = telebot.TeleBot(BOT_ID)


@bot.message_handler(commands=['zachem?'])
def send_message(message):
    bot.send_message(message.chat.id, 'Зачем? Почему? А я че бот,  я е*у что ли ? ')


bot.polling(none_stop=True)
