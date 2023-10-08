import os
from dotenv import load_dotenv
from pyrogram import Client, filters  # телеграм клиент
from telebot import types
import telebot
import os

load_dotenv()

BOT_ID = os.getenv("BOT_ID")
bot = telebot.TeleBot(BOT_ID)
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

PRIVATE_PUBLIC = os.getenv("PRIVATE_PUBLIC")  # скрытый паблик для управления ботом
PUBLIC_PUBLIC = os.getenv("PUBLIC_PUBLIC")  # паблик куда будем репостить
SOURCE_PUBLICS = [
    # список пабликов-доноров, откуда бот будет пересылать посты
    'mudak',
    'zagruz12'

]
PHONE_NUMBER = os.getenv("PHONE_NUMBER")  # номер зарегистрованный в телеге

media_group_id = 0
app = Client("posts_collector", api_id=API_ID, api_hash=API_HASH,
             phone_number=PHONE_NUMBER)

last_media_group_id = None
count = 1


@app.on_message(filters.chat(SOURCE_PUBLICS))
def new_channel_post(client, message):
    global last_media_group_id, count
    button_foo = types.InlineKeyboardButton('Foo', callback_data='foo')
    button_bar = types.InlineKeyboardButton('Bar', callback_data='bar')

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(button_foo)
    keyboard.add(button_bar)

    # Check if the message is part of a media group and the media group ID is different
    if message.media_group_id:
        # Save the new media_group_id
        if message.media_group_id != last_media_group_id:
            last_media_group_id = message.media_group_id
            count = 1
            # Process the media group (e.g., copy it to the destination chat)
            client.copy_media_group(PRIVATE_PUBLIC, message.chat.id, message.id)
            bot.send_message(PRIVATE_PUBLIC, text='Keyboard example', reply_markup=keyboard)
        else:
            count = count + 1
    else:
        client.copy_message(PRIVATE_PUBLIC, message.chat.id, message.id)
        bot.send_message(PRIVATE_PUBLIC, text='Keyboard example', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    bot.edit_message_text('Отправлено', call.message.chat.id, call.message.id)


@app.on_edited_message(filters.chat(PRIVATE_PUBLIC))
def post_in_public(client, message):
    client.copy_media_group(-1001813831972, message.chat.id, message.id - 1)


if __name__ == '__main__':
    print('Atempt to run Pyrogram')
    app.run()  # эта строка запустит все обработчики
