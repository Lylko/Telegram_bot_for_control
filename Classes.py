from mysql.connector import connect, Error
import config

class MySQL:

    def __init__(self):
        """Подключаемся к БД и сохраняем курсор соединения"""
        try:
            self.connection = config.Server_data
        except:
            print('Connection failed')
        self.cursor = self.connection.cursor()


    def user_exist(self, user_id):
        """Проверяем, есть ли уже юзер в базе"""
        
        self.cursor.execute('SELECT * FROM `test` WHERE `user_id` = {}'.format(user_id))
        result = self.cursor.fetchall()
        return bool(len(result))

    def add_subscriber(self,user_id):
        """Добавление нового пользователя программы."""
        self.cursor.execute("INSERT INTO `test` (`user_id`, `status`, `command`) VALUES({},{},{})".format(user_id, 0, 0))
        return self.connection.commit()


    def check_parametrs(self,user_id):
        """Проверяем значение параметров юзера"""
        self.cursor.execute('SELECT * FROM `test` WHERE `user_id` = {}'.format(user_id))
        return (self.cursor.fetchall())


    def update_status(self, user_id, status):
        """Включение/выключение управления"""
        return self.cursor.execute("UPDATE `test` SET `status` = {} WHERE `user_id` = {}".format(status, user_id))


    def send_command(self, user_id, command):
        """Отправка команды"""
        return self.cursor.execute("UPDATE `test` SET `command` = {} WHERE `user_id` = {}".format(command, user_id))

    def commit(self):
        self.connection.commit()

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()