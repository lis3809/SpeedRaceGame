import sqlite3


class DBManager:
    def __init__(self):
        # Создаем подключение к базе данных
        self.connection = sqlite3.connect('db_players.db')
        self.cursor = self.connection.cursor()
        # Создаем таблицу Users
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        score INTEGER DEFAULT 0)
        ''')
        # Сохраняем изменения и закрываем соединение
        self.connection.commit()

    def save_new_player(self, name):
        try:
            self.cursor.execute('''
                        INSERT INTO players (name)
                        VALUES (?)
                    ''', (name,))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            print("Такой пользователь уже зарегистрирован")
            return False

    def get_user_score(self, name):
        self.cursor.execute('''
            SELECT score
            FROM players
            WHERE name=?
        ''', (name,))
        user_score = self.cursor.fetchone()
        return user_score[0]

    def update_player_data(self, name, score):
        self.cursor.execute('''UPDATE players 
                        SET score=?
                        WHERE name=?
                    ''', (score, name))
        # Сохраняем изменения и закрываем соединение
        self.connection.commit()

    def get_top_5_users(self):
        limit = 5
        self.cursor.execute('''
            SELECT name, score
            FROM players
            ORDER BY score DESC
            LIMIT ?
        ''', (limit,))
        top_5_users = self.cursor.fetchall()
        return top_5_users

    def get_best_player_score(self):
        self.cursor.execute('''
                    SELECT MAX (score)
                    FROM players
                ''')
        best_player_score = self.cursor.fetchone()
        return best_player_score[0]

    def close_connection(self):
        self.connection.close()
