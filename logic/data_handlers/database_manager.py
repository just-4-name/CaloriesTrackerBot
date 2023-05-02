import aiosqlite


async def start_db():
    async with aiosqlite.connect('tracker_database') as db:
        async with await db.cursor() as cur:
            await cur.execute("CREATE TABLE IF NOT EXISTS users_goals (user_id INT PRIMARY KEY, name TEXT,"
                              " calories_goal INT, proteins_goal INT, carbs_goal INT, fats_goal INT)")
            await cur.execute("CREATE TABLE IF NOT EXISTS users_macros (user_id INT PRIMARY KEY, name TEXT,"
                              " calories INT, proteins INT, carbs INT, fats INT)")
        await db.commit()


async def create_user(user_id, user_name):
    async with aiosqlite.connect('tracker_database') as db:
        async with await db.cursor() as cur:
            user_in_goals = await (
                await cur.execute(f'SELECT 1 FROM users_goals WHERE user_id == {user_id}')).fetchone()
            if not user_in_goals:
                await cur.execute('INSERT INTO users_goals VALUES(?, ?, ?, ?, ?, ?)', (user_id, user_name, 0, 0, 0, 0))
            user_in_macros = await (
                await cur.execute(f'SELECT 1 FROM users_macros WHERE user_id == {user_id}')).fetchone()
            if not user_in_macros:
                await cur.execute('INSERT INTO users_macros VALUES(?, ?, ?, ?, ?, ?)', (user_id, user_name, 0, 0, 0, 0))
        await db.commit()


async def edit_user_macros(user_id, data):
    async with aiosqlite.connect('tracker_database') as db:
        async with await db.cursor() as cur:
            await cur.execute(
                f'UPDATE users_macros SET calories = calories + {data["calories"]}, proteins = proteins + '
                f'{data["protein_g"]}, carbs = carbs + {data["carbohydrates_total_g"]}, fats = fats + '
                f'{data["fat_total_g"]} WHERE user_id == {user_id}')
        await db.commit()


async def annul_user_macros(user_id):
    async with aiosqlite.connect('tracker_database') as db:
        async with await db.cursor() as cur:
            await cur.execute(
                f'UPDATE users_macros SET calories = 0, proteins = 0, carbs = 0, fats = 0 WHERE user_id == {user_id}')
        await db.commit()


async def edit_user_goals(user_id, data):
    async with aiosqlite.connect('tracker_database') as db:
        async with await db.cursor() as cur:
            await cur.execute(
                f'UPDATE users_goals SET calories_goal = {data["calories"]}, proteins_goal = {data["proteins"]},'
                f' carbs_goal = {data["carbs"]}, fats_goal = {data["fats"]} WHERE user_id == {user_id}')
        await db.commit()


async def get_daily_macros(user_id):
    async with aiosqlite.connect('tracker_database') as db:
        async with await db.cursor() as cur:
            await cur.execute(f"SELECT calories, proteins, carbs, fats FROM users_macros WHERE user_id == {user_id}")
            calories, proteins, carbs, fats = await cur.fetchone()
            return {'calories': calories, 'protein_g': proteins, 'carbohydrates_total_g': carbs, 'fat_total_g': fats}


async def get_achievements(user_id):
    async with aiosqlite.connect('tracker_database') as db:
        async with await db.cursor() as cur:
            await cur.execute(f"SELECT calories_goal, proteins_goal, carbs_goal, fats_goal FROM users_goals "
                              f"WHERE user_id == {user_id}")
            calories_goal, proteins_goal, carbs_goal, fats_goal = await cur.fetchone()
            if calories_goal == 0:
                return None
            await cur.execute(f"SELECT calories, proteins, carbs, fats FROM users_macros WHERE user_id == {user_id}")
            calories, proteins, carbs, fats = await cur.fetchone()
            return {'calories_goal': calories_goal, 'proteins_goal': proteins_goal, 'carbs_goal': carbs_goal,
                    'fats_goal': fats_goal, 'calories': calories, 'proteins': proteins, 'carbs': carbs,
                    'fats': fats}

