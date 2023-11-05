import os
from dotenv import load_dotenv
from pyrogram import Client, filters  # телеграм клиент
from telebot import types
import telebot
import os
import time

load_dotenv()

BOT_ID = os.getenv("BOT_ID")
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

PRIVATE_PUBLIC = int(os.getenv("PRIVATE_PUBLIC"))  # скрытый паблик для управления ботом
PUBLIC_PUBLIC = os.getenv("PUBLIC_PUBLIC")  # паблик куда будем репостить
SOURCE_PUBLICS = [
    # список пабликов-доноров, откуда бот будет пересылать посты
    'mudak',
    'zagruz12'
]

PHONE_NUMBER = os.getenv("PHONE_NUMBER")  # номер зарегистрованный в телеге

app = Client("posts_collector", api_id=API_ID, api_hash=API_HASH,
             phone_number=PHONE_NUMBER)
bot = telebot.TeleBot(BOT_ID)

last_media_group_id = None
count = 1


@app.on_message(filters.chat(SOURCE_PUBLICS))
def new_channel_post(client, message):
    global last_media_group_id, count
    button_send = types.InlineKeyboardButton('Отправить ✅', callback_data='Отправлено')
    button_delete = types.InlineKeyboardButton('Удалить  ❌', callback_data='Удалено')

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(button_send)
    keyboard.add(button_delete)

    print(message)
    # Check if the message is part of a media group and the media group ID is different
    if message.media_group_id:
        # Save the new media_group_id
        if message.media_group_id != last_media_group_id:
            last_media_group_id = message.media_group_id
            count = 1
            # Process the media group (e.g., copy it to the destination chat)
            client.copy_media_group(PRIVATE_PUBLIC, message.chat.id, message.id)
            bot.send_message(PRIVATE_PUBLIC, text='Выберите действие', reply_markup=keyboard)
        else:
            count = count + 1
    else:
        client.copy_message(PRIVATE_PUBLIC, message.chat.id, message.id)
        bot.send_message(PRIVATE_PUBLIC, text='Выберите действие', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    bot.edit_message_text(call.data, call.message.chat.id, call.message.id)


@app.on_edited_message(filters.chat(PRIVATE_PUBLIC))
def post_in_public(client, message):

    code = message.text

    if code == "Удалено":
        try:
            media_group_messages = client.get_media_group(message.chat.id, message.id - 1)
            for media_message in media_group_messages:
                bot.delete_message(media_message.chat.id, media_message.id )
        except ValueError:
            bot.delete_message(message.chat.id, message.id - 1)
        time.sleep(3)
        bot.delete_message(message.chat.id, message.id)

    elif code == "Отправлено":
        try:
            client.copy_media_group(PRIVATE_PUBLIC, message.chat.id, message.id - 1)
        except ValueError:
            bot.copy_message(PRIVATE_PUBLIC, message.chat.id, message.id - 1)
        bot.delete_message(message.chat.id, message.id)


if __name__ == '__main__':
    print('Atempt to run Pyrogram')
    app.run()  # эта строка запустит все обработчики
