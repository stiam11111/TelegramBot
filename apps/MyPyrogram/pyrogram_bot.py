import os
from dotenv import load_dotenv
from pyrogram import Client, filters  # телеграм клиент
from apps.DB_actions import data_base
from apps.MyTelebot.bot import myTeleBot

load_dotenv()

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

class PyrogramBot:
    # Создать можно на my.telegram.org
    # создаем клиент телеграм
    app = Client("posts_collector", api_id=API_ID, api_hash=API_HASH,
                 phone_number=PHONE_NUMBER)
    last_media_group_id = None
    count = 1


    @app.on_message(filters.chat(SOURCE_PUBLICS))
    def new_channel_post(client, message):
        # Check if the message is part of a media group and the media group ID is different
        if message.media_group_id :
            # Save the new media_group_id
            if  message.media_group_id != PyrogramBot.last_media_group_id:
                PyrogramBot.last_media_group_id = message.media_group_id
                PyrogramBot.count = 1
                # Process the media group (e.g., copy it to the destination chat)
                client.copy_media_group(-1001813831972, message.chat.id, message.id)
                myTeleBot.bot.send_message(-1001813831972, message.media_group_id)
            else :
                PyrogramBot.count = PyrogramBot.count + 1
        else:
            client.copy_message(-1001813831972, message.chat.id, message.id)
            myTeleBot.bot.send_message(-1001813831972, '1')

    @app.on_message(filters.chat(-1001813831972))
    def post_request(client, message):
        print()
        count = PyrogramBot.count
        while count > 0:
            myTeleBot.bot.copy_message(myTeleBot.client_chat_id, message.chat.id, message.id - count)
            count = count -1



pyrogram_bot = PyrogramBot()

