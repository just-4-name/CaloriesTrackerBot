import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import BotCommand, Message

from logic.config_reader import load_config
from logic.handlers.common import register_common_handlers
from logic.handlers.set_goals import register_goals_handlers
from logic.handlers.add_meals import register_add_meal_handlers
from logic.handlers.add_custom import register_add_custom_handlers
from logic.data_handlers.database_manager import start_db
from logic.data_handlers.site_parser import FoodSearcher


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='/start', description='Start bot'),
        BotCommand(command='/set_goals', description='Set Nutrition Goals'),
        BotCommand(command='/add', description='Add meal'),
        BotCommand(command='/today', description='Learn macros for today'),
        BotCommand(command='/achieved', description='Your achievements for today'),
        BotCommand(command='/new_day', description='Start new day (annul all macros)'),
        BotCommand(command='/add_custom', description='Add custom meal and enter its macros'),
        BotCommand(command='/cancel', description='Cancel'),
        BotCommand(command='/help', description='Help')
    ]
    await bot.set_my_commands(commands)


class DpMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: Message, data: dict):
        data["food_searcher"] = FoodSearcher()


async def main():
    logging.basicConfig(level=logging.INFO)
    config = load_config("config/bot.ini")

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(bot, storage=MemoryStorage())
    dp.middleware.setup(DpMiddleware())
    await start_db()

    register_common_handlers(dp)
    register_goals_handlers(dp)
    register_add_meal_handlers(dp)
    register_add_custom_handlers(dp)

    await set_commands(bot)
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
