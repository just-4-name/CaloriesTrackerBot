import json

import requests
from logic.config_reader import load_config


class FoodSearcher:
    def __init__(self):
        self.__config = load_config('config/bot.ini')
        self.__url = 'https://api.api-ninjas.com/v1/nutrition'

    async def search_food(self, food_name, gram_num):
        query = f'{gram_num}g {food_name}'
        api_url = f'{self.__url}?query={query}'
        response = requests.get(api_url, headers={'X-Api-Key': self.__config.parser.api_key})
        if response.status_code == requests.codes.ok:
            data = json.loads(str(response.text))[0]
            return data
        else:
            print("Error:", response.status_code, response.text)

    async def check_if_in_db(self, food_name):
        api_url = f'{self.__url}?query={food_name}'
        response = requests.get(api_url, headers={'X-Api-Key': self.__config.parser.api_key})
        return response.status_code == requests.codes.ok
