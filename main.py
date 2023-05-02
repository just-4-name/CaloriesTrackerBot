import time
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from logic.data_handlers.database_manager import DataBaseManager

TOKEN = '5896232132:AAHfxghll1ETFWPOLafgcRtPHAQ2SYOVRIo'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)
db_manager = DataBaseManager()


def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_first_name = message.from_user.first_name
    logging.info(f'{user_id=} {user_first_name=} {time.asctime()}')
    await db_manager.create_user(user_id, user_first_name)
    await message.reply(f"Hello, {user_first_name}")

    # for i in range(30):
    #     time.sleep(1)
    #
    #     await bot.send_message(user_id, 'test')

dp.register_message_handler(entry_point, commands=['Set Nutrition Goals'])

if __name__ == '__main__':
    executor.start_polling(dp)
