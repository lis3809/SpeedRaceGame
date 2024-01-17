import sqlite3


class DBManager:

    def __init__(self):
        # Создаем подключение к базе данных
        self.__connection = sqlite3.connect('db_players.db')
        self.__cursor = self.__connection.cursor()
        # Создаем таблицу Users
        self.__cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        score INTEGER DEFAULT 0)
        ''')
        # Сохраняем изменения и закрываем соединение
        self.__connection.commit()

    def save_new_player(self, name):
        try:
            self.__cursor.execute('''
                        INSERT INTO players (name)
                        VALUES (?)
                    ''', (name,))
            self.__connection.commit()
            return True
        except sqlite3.IntegrityError:
            print("Такой пользователь уже зарегистрирован")
            return False

    def get_user_score(self, name):
        self.__cursor.execute('''
            SELECT score
            FROM players
            WHERE name=?
        ''', (name,))
        user_score = self.__cursor.fetchone()
        return user_score[0]

    def update_player_data(self, name, score):
        self.__cursor.execute('''UPDATE players 
                        SET score=?
                        WHERE name=?
                    ''', (score, name))
        # Сохраняем изменения и закрываем соединение
        self.__connection.commit()

    def get_top_5_users(self):
        limit = 5
        self.__cursor.execute('''
            SELECT name, score
            FROM players
            ORDER BY score DESC
            LIMIT ?
        ''', (limit,))
        top_5_users = self.__cursor.fetchall()
        return top_5_users

    def get_best_player_score(self):
        self.__cursor.execute('''
                    SELECT MAX (score)
                    FROM players
                ''')
        best_player_score = self.__cursor.fetchone()
        return best_player_score[0]

    def close_connection(self):
        self.__connection.close()
