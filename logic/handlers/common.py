from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from logic.data_handlers.database_manager import create_user, get_daily_macros, get_achievements, annul_user_macros
from logic.data_handlers.formatter import format_data, format_achievements
from resources.messages import HELP_MESSAGE, ASK_ENTER_GOALS_MESSAGE, NEW_DAY_MESSAGE, hello_message


async def start(message: types.Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    user_first_name = message.from_user.first_name
    await create_user(user_id, user_first_name)
    await message.answer(await hello_message(user_first_name))


async def learn_daily_macros(message: types.Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    data = await get_daily_macros(user_id)
    await message.answer(f'Today your macros are: {await format_data(data)}')


async def cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Action cancelled')


async def learn_achievements(message: types.Message, state: FSMContext):
    await state.finish()
    data = await get_achievements(message.from_user.id)
    if data is None:
        await message.answer(ASK_ENTER_GOALS_MESSAGE)
        return
    await message.answer(f'Today, your achievements are {await format_achievements(data)}')


async def start_new_day(message: types.Message, state: FSMContext):
    await state.finish()
    await annul_user_macros(message.from_user.id)
    await message.answer(NEW_DAY_MESSAGE)


async def cmd_help(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(HELP_MESSAGE)


def register_common_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands='start', state='*')
    dp.register_message_handler(learn_daily_macros, commands='today', state='*')
    dp.register_message_handler(cancel, commands='cancel', state='*')
    dp.register_message_handler(learn_achievements, commands='achieved', state='*')
    dp.register_message_handler(start_new_day, commands='new_day', state='*')
    dp.register_message_handler(help, commands='help', state='*')
