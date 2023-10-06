import os
from dotenv import load_dotenv
from pyrogram import Client, filters  # телеграм клиент
from apps.DB_actions import data_base

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


class PyrogramBot:
    # Создать можно на my.telegram.org

    # создаем клиент телеграм
    app = Client("posts_collector", api_id=API_ID, api_hash=API_HASH,
                 phone_number=PHONE_NUMBER)

    # обработчик нового сообщения
    # вызывается при появлении нового поста в одном из пабликов-доноров
    @app.on_message(filters.chat(SOURCE_PUBLICS))
    def new_channel_post(client, message):
        # сохраняем пост в базу (функцию add_post_to_db определим потом)
        post_id = data_base.add_post_to_db(message)

        # пересылаем пост в скрытый паблик
        message.forward(PRIVATE_PUBLIC)

        # в скрытый паблик отправляем присвоенный id поста
        client.send_message(PRIVATE_PUBLIC, post_id)
        # потом для пересылки в публичный паблик админ должен отправить боту этот id

    # обработчик нового сообщения из скрытого паблика
    # если админ пишет в паблик `132+` это значит переслать пост с id = 132 в публичный паблик

    @app.on_message(filters.chat(PRIVATE_PUBLIC)
                    & filters.regex(r'\d+\+')  # фильтр текста сообщения `{число}+`
                    )
    def post_request(client, message):
        # получаем id поста из сообщения (обрезаем "+" в конце)
        post_id = str(message.text).strip('+')
        # получаем из базы пост по этому id
        post = data_base.db.get(post_id)
        if post is None:
            # если нет в базе пишем в скрытый паблик ошибку
            client.send_message(PRIVATE_PUBLIC,
                                '`ERROR NO POST ID IN DB`')
            # и выходим
            return

        try:
            # по данным из базы, получаем pyrogram обьект сообщения
            #
            # message_id = (post['message_id'] * -1) - 1000000000000

            msg = client.get_messages(post['username'], post['message_id'])
            # пересылаем его в паблик
            # as_copy=True значит, что мы не будем отображать паблик донор, будто это наш пост XD

            msg.copy(PUBLIC_PUBLIC)
            # отправляем сообщение в скрытый паблик о успехе
            client.send_message(PRIVATE_PUBLIC, f'`SUCCESS REPOST!`')
        except Exception as e:
            # если произойдет какая-то ошибка в 3 строчках выше - сообщим админу
            client.send_message(PRIVATE_PUBLIC, f'`ERROR {e}`')


pyrogram_bot = PyrogramBot()
