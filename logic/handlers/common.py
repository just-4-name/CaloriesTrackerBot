from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter

from logic.data_handlers.database_manager import DataBaseManager
from logic.data_handlers.formatter import format_data


async def start(message: types.Message, state: FSMContext, db_manager: DataBaseManager):
    await state.finish()
    user_id = message.from_user.id
    user_first_name = message.from_user.first_name
    await db_manager.create_user(user_id, user_first_name)
    await message.answer(f"Hello, {user_first_name}!")


async def learn_daily_macros(message: types.Message, state: FSMContext, db_manager: DataBaseManager):
    await state.finish()
    user_id = message.from_user.id
    data = await db_manager.get_daily_macros(user_id)
    await message.answer(f'Today your macros are: {await format_data(data)}')


def register_common_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands='start', state='*')
    dp.register_message_handler(learn_daily_macros, commands='today', state='*')
