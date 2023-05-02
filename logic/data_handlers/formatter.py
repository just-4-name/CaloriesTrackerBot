async def format_data(data):
    return f"\n- {data['calories']} calories\n- {data['protein_g']} grams of protein\n- {data['carbohydrates_total_g']}" \
           f" grams of carbs\n- {data['fat_total_g']} grams of fats"
