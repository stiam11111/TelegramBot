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
    # обработчик нового сообщения
    # вызывается при появлении нового поста в одном из пабликов-доноров

    # @app.on_message(filters.chat(SOURCE_PUBLICS))
    # def new_channel_post(client, message):
    #     # сохраняем пост в базу (функцию add_post_to_db определим потом)
    #     global media_group_id
    #     post_id = data_base.add_post_to_db(message)
    #     # пересылаем пост в скрытый паблик
    #     print(message)
    #     if message.media_group_id:
    #         client.copy_media_group(-1001813831972, message.chat.id, message.id)
    #         if media_group_id != message.media_group_id:
    #             media_group_id = message.media_group_id
    #             myTeleBot.bot.send_message(-1001813831972, media_group_id)
    #     else:
    #         client.copy_message(-1001813831972, message.chat.id, message.id)
    #         myTeleBot.bot.send_message(-1001813831972, '1')

    @app.on_message(filters.chat(SOURCE_PUBLICS))
    def new_channel_post(client, message):
        # Check if the message is part of a media group and the media group ID is different
        if message.media_group_id and message.media_group_id != PyrogramBot.last_media_group_id:
            # Save the new media_group_id
            PyrogramBot.last_media_group_id = message.media_group_id
            PyrogramBot.count = 1
            # Process the media group (e.g., copy it to the destination chat)
            client.copy_media_group(-1001813831972, message.chat.id, message.id)
            myTeleBot.bot.send_message(-1001813831972, message.media_group_id)

        else :
            PyrogramBot.count = PyrogramBot.count + 1

    # потом для пересылки в публичный паблик админ должен отправить боту этот id

    # обработчик нового сообщения из скрытого паблика
    # если админ пишет в паблик `132+` это значит переслать пост с id = 132 в публичный паблик

    @app.on_message(filters.chat(-1001813831972))
    def post_request(client, message):
        print()
        count = PyrogramBot.count
        while count > 0:
            myTeleBot.bot.copy_message(myTeleBot.client_chat_id, message.chat.id, message.id - count)
            count = count -1



pyrogram_bot = PyrogramBot()


# получаем из базы пост по этому id
        # post = data_base.db.get(post_id)
        # print(message)
        # if post is None:
        #     # если нет в базе пишем в скрытый паблик ошибку
        #     client.send_message(PRIVATE_PUBLIC,
        #                         '`ERROR NO POST ID IN DB`')
        #     # и выходим
        #     return
        #
        # try:
        #     # по данным из базы, получаем pyrogram обьект сообщения
        #     #
        #     # message_id = (post['message_id'] * -1) - 1000000000000
        #
        #     msg = client.get_messages(post['username'], post['message_id'])
        #     # пересылаем его в паблик
        #     # as_copy=True значит, что мы не будем отображать паблик донор, будто это наш пост XD
        #
        #     msg.copy(PUBLIC_PUBLIC)
        #     # отправляем сообщение в скрытый паблик о успехе
        #     client.send_message(PRIVATE_PUBLIC, f'`SUCCESS REPOST!`')
        # except Exception as e:
        #     # если произойдет какая-то ошибка в 3 строчках выше - сообщим админу
        #     client.send_message(PRIVATE_PUBLIC, f'`ERROR {e}`')
