import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import BotCommand, Message
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from logic.config_reader import load_config
from logic.handlers.common import register_common_handlers
from logic.handlers.set_goals import register_goals_handlers
from logic.handlers.add_meals import register_add_meal_handlers
from logic.data_handlers.database_manager import DataBaseManager
from logic.data_handlers.site_parser import FoodSearcher

logger = logging.getLogger(__name__)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='/set_goals', description='Set Nutrition Goals'),
        BotCommand(command='/start', description='Start bot'),
        BotCommand(command='/add', description='Add meal'),
        BotCommand(command='/today', description='Learn macros for today')
    ]
    await bot.set_my_commands(commands)


class YourMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: Message, data: dict):
        # `text` is a name of var passed to handler
        data["db_manager"] = DataBaseManager()
        data["food_searcher"] = FoodSearcher()


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")

    config = load_config("config/bot.ini")

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(bot, storage=MemoryStorage())
    dp.middleware.setup(YourMiddleware())

    register_common_handlers(dp)
    register_goals_handlers(dp)
    register_add_meal_handlers(dp)

    await set_commands(bot)
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
