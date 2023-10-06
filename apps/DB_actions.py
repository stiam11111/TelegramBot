import shelve  # файловая база данных


# функция сохранения поста в бд
# генерирует уникальный id для поста и возвратит этот id


class DataBase:
    db = shelve.open('data_base/data.db', writeback=True)

    def add_post_to_db(self, message):
        try:
            # генерируем уникальный id для поста, равен максимальному в базе + 1
            new_id = max(int(k) for k in self.db.keys()
                         if k.isdigit()) + 1

        except:
            # если постов еще нет в базе вылетит ошибка и мы попадем сюда
            # тогда id ставим = 1
            new_id = 1

        # запись в базу необходимой информации про пост
        # Обратите внимание, shelve поддеживает только строковые ключи

        self.db[str(new_id)] = {
            'username': message.chat.username,  # паблик-донор
            'message_id': message.id,  # внутренний id сообщения

        }
        return new_id


data_base = DataBase()