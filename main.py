import telebot

bot = telebot.TeleBot('6274545389:AAFo4lEw4oe3kQ-o4kuYKRW85ypZ0BtT7_A')


@bot.message_handler(commands=['zachem?'])
def send_message(message):
    bot.send_message(message.chat.id, 'Зачем? Почему? А я че бот,  я е*у что ли ? ')


bot.polling(none_stop=True)