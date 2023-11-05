import os
from dotenv import load_dotenv
from pyrogram import Client, filters  # телеграм клиент
from telebot import types
import telebot
import os
import time

load_dotenv()


class PyrogramBot:
    def __init__(self):
        self.BOT_ID = os.getenv("BOT_ID")
        self.API_ID = os.getenv("API_ID")
        self.API_HASH = os.getenv("API_HASH")
        self.PHONE_NUMBER = os.getenv("PHONE_NUMBER")  # номер зарегистрованный в телеге
        self.PRIVATE_PUBLIC = int(os.getenv("PRIVATE_PUBLIC"))  # скрытый паблик для управления ботом
        self.PUBLIC_PUBLIC = os.getenv("PUBLIC_PUBLIC")  # паблик куда будем репостить
        self.SOURCE_PUBLICS = [
            # список пабликов-доноров, откуда бот будет пересылать посты
            'mudak',
            'zagruz12'
        ]

        self._create_app()
        self._create_bot()

        self.last_media_group_id = None
        self.count = 1

        self.run_events_listeners()

    def _create_app(self):
        self.app = Client("posts_collector", api_id=self.API_ID, api_hash=self.API_HASH,
                          phone_number=self.PHONE_NUMBER)

    def run_pyrogram(self):
        self.app.run()
        print('Atempt to run Pyrogram')

    def _create_bot(self):
        self.bot = telebot.TeleBot(self.BOT_ID)

    def run_telebot(self):
        print('Atempt to run TeleBot')
        self.bot.polling(none_stop=True)

    def run_events_listeners(self):

        @self.app.on_message(filters.chat(self.SOURCE_PUBLICS))
        def new_channel_post(client, message):

            button_send = types.InlineKeyboardButton('Отправить ✅', callback_data='Отправлено')
            button_delete = types.InlineKeyboardButton('Удалить  ❌', callback_data='Удалено')

            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(button_send)
            keyboard.add(button_delete)

            print('Price= ', self.__price_parser('Hello world aljfskdflsadkj 24.8$'))
            # Check if the message is part of a media group and the media group ID is different
            if message.media_group_id:
                # Save the new media_group_id
                if message.media_group_id != self.last_media_group_id:
                    self.last_media_group_id = message.media_group_id
                    self.count = 1
                    # Process the media group (e.g., copy it to the destination chat)
                    client.copy_media_group(self.PRIVATE_PUBLIC, message.chat.id, message.id)
                    self.bot.send_message(self.PRIVATE_PUBLIC, text='Выберите действие', reply_markup=keyboard)
                else:
                    self.count = self.count + 1
            else:
                client.copy_message(self.PRIVATE_PUBLIC, message.chat.id, message.id)
                self.bot.send_message(self.PRIVATE_PUBLIC, text='Выберите действие', reply_markup=keyboard)

        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_handler(call):
            self.bot.edit_message_text(call.data, call.message.chat.id, call.message.id)

        @self.app.on_edited_message(filters.chat(self.PRIVATE_PUBLIC))
        def post_in_public(client, message):

            code = message.text

            if code == "Удалено":
                try:
                    media_group_messages = client.get_media_group(message.chat.id, message.id - 1)
                    for media_message in media_group_messages:
                        self.bot.delete_message(media_message.chat.id, media_message.id)
                except ValueError:
                    self.bot.delete_message(message.chat.id, message.id - 1)
                time.sleep(3)
                self.bot.delete_message(message.chat.id, message.id)

            elif code == "Отправлено":
                try:
                    client.copy_media_group(self.PRIVATE_PUBLIC, message.chat.id, message.id - 1)
                except ValueError:
                    self.bot.copy_message(self.PRIVATE_PUBLIC, message.chat.id, message.id - 1)
                self.bot.delete_message(message.chat.id, message.id)

    def __price_parser(self, description):
        price_end = description.find('$')
        if price_end != -1:
            i = 1
            template = '1234567890,.'

            while description[price_end - i]  in template:
                i = i + 1
            price_start = price_end - i + 1
            print('start ', price_start )
            print('start ', price_end)

            return description[price_start:price_end]+'$'
        else:
            return ''
