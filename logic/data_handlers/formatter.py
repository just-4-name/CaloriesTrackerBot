from logic.data_handlers.valid_checker import is_float


async def round_values(data):
    rounded_data = dict()
    for key, value in data.items():
        if await is_float(value):
            rounded_data[key] = round(float(value))
    return rounded_data


async def format_data(data):
    data = await round_values(data)
    return f"\n- {data['calories']} calories\n- {data['protein_g']} grams of protein\n- " \
           f"{data['carbohydrates_total_g']} grams of carbs\n- {data['fat_total_g']} grams of fats"


async def get_diff_type(data, key):
    return ('surplus: ' if (data[key] > data[key + '_goal']) else 'deficit: ') \
       + str(abs(data[key] - data[key + '_goal'])) + ('cal' if key == 'calories' else 'g')


async def format_achievements(data):
    data = await round_values(data)
    return f"\n- Calories: {data['calories']}/{data['calories_goal']}, {await get_diff_type(data, 'calories')}" \
           f"\n- Proteins: {data['proteins']}/{data['proteins_goal']}, {await get_diff_type(data, 'proteins')}" \
           f"\n- Carbs: {data['carbs']}/{data['carbs_goal']}, {await get_diff_type(data, 'carbs')}" \
           f"\n- Fats: {data['fats']}/{data['fats_goal']}, {await get_diff_type(data, 'fats')}"
