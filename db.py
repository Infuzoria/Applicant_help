import sqlite3

class BotDB:

    def __init__(self, db_file):
        """
        Инициализация соединения с БД
        """
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        """
        Проверяем, есть ли пользователь в БД
        """
        result = self.cursor.execute("SELECT * FROM 'users'")
        for i in result.fetchall():
            if i[1] == user_id:
                return True
        return False

    def get_user_id(self, user_id):
        """
        Получаем id пользователя в базе по его id в телеграмме
        """
        result = self.cursor.execute("SELECT 'id' FROM 'users' WHERE 'user_id' = ?", (user_id,))
        return result.fetchone()[0]

    def get_snils(self, user_id):
        """
        Получаем СНИЛС пользователя в базе по его id в телеграмме
        """
        result = self.cursor.execute("SELECT * FROM 'users'")
        for i in result.fetchall():
            if i[1] == user_id:
                if i[3] is None:
                    return "NULL"
                else:
                    return i[3]

    def add_snils(self, user_id, snils):
        """
        Добавляем СНИЛС пользователя в БД
        """
        self.cursor.execute("UPDATE users SET snils = ? WHERE user_id = ?", (snils, user_id,))
        return self.conn.commit()

    def add_user(self, user_id):
        """
        Добавляем пользователя в БД
        """
        self.cursor.execute("INSERT INTO 'users' ('user_id') VALUES (?)", (user_id,))
        return self.conn.commit()
