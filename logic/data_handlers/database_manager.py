import sqlite3 as sq


class DataBaseManager:

    def __init__(self):
        self.__connection = sq.connect('tracker_database')
        self.__cursor = self.__connection.cursor()
        self.start_db()

    def start_db(self):
        self.__cursor.execute("CREATE TABLE IF NOT EXISTS users_goals (user_id INT PRIMARY KEY, name TEXT,"
                              " calories_goal INT, proteins_goal INT, carbs_goal INT, fats_goal INT)")
        self.__cursor.execute("CREATE TABLE IF NOT EXISTS users_macros (user_id INT PRIMARY KEY, name TEXT,"
                              " calories INT, proteins INT, carbs INT, fats INT)")
        self.__connection.commit()

    async def create_user(self, user_id, user_name):
        user = self.__cursor.execute(f'SELECT 1 FROM users_goals WHERE user_id == {user_id}').fetchone()
        if not user:
            self.__cursor.execute('INSERT INTO users_goals VALUES(?, ?, ?, ?, ?, ?)', (user_id, user_name, 0, 0, 0, 0))
            self.__cursor.execute('INSERT INTO users_macros VALUES(?, ?, ?, ?, ?, ?)', (user_id, user_name, 0, 0, 0, 0))
            self.__connection.commit()

    async def edit_user_goals(self, user_id, data):
        self.__cursor.execute(
            f'UPDATE users_goals SET calories_goal = {data["calories"]}, proteins_goal = {data["proteins"]},'
            f' carbs_goal = {data["carbs"]}, fats_goal = {data["fats"]} WHERE user_id == {user_id}')
        self.__connection.commit()

    async def edit_user_macros(self, user_id, data):
        self.__cursor.execute(
            f'UPDATE users_macros SET calories = calories + {data["calories"]}, proteins = proteins + '
            f'{data["protein_g"]}, carbs = carbs + {data["carbohydrates_total_g"]}, fats = fats + '
            f'{data["fat_total_g"]} WHERE user_id == {user_id}')
        self.__connection.commit()

    async def get_daily_macros(self, user_id):
        with self.__connection:
            self.__cursor.execute(f"SELECT calories, proteins, carbs, fats FROM users_macros WHERE user_id == {user_id}")
            calories, proteins, carbs, fats = self.__cursor.fetchone()
            return {'calories': calories, 'protein_g': proteins, 'carbohydrates_total_g': carbs, 'fat_total_g': fats}

    def __del__(self):
        self.__connection.close()
