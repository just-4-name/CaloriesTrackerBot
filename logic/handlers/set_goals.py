from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from logic.data_handlers.database_manager import edit_user_goals
from logic.data_handlers.valid_checker import is_positive_int
from resources.messages import ENTER_POS_INT_MESSAGE


class SetGoal(StatesGroup):
    waiting_for_calories_num = State()
    waiting_for_proteins_num = State()
    waiting_for_carbs_num = State()
    waiting_for_fats_num = State()


async def enter_calories_goal(message: types.Message, state: FSMContext):
    await message.answer('Please, enter daily calories goal below:')
    await state.set_state(SetGoal.waiting_for_calories_num.state)


async def calories_goal_chosen(message: types.Message, state: FSMContext):
    if not await is_positive_int(message.text):
        await message.answer(ENTER_POS_INT_MESSAGE)
        return
    await state.update_data(calories=int(message.text))
    await state.set_state(SetGoal.waiting_for_proteins_num.state)
    await message.answer('Great! Next step - enter your grams of protein goal:')


async def proteins_goal_chosen(message: types.Message, state: FSMContext):
    if not await is_positive_int(message.text):
        await message.answer(ENTER_POS_INT_MESSAGE)
        return
    await state.update_data(proteins=int(message.text))
    await state.set_state(SetGoal.waiting_for_carbs_num.state)
    await message.answer('Great! Next step - enter your grams of carbs goal:')


async def carbs_goal_chosen(message: types.Message, state: FSMContext):
    if not await is_positive_int(message.text):
        await message.answer(ENTER_POS_INT_MESSAGE)
        return
    await state.update_data(carbs=int(message.text))
    await state.set_state(SetGoal.waiting_for_fats_num.state)
    await message.answer('Great! Next step - enter your grams of fats goal:')


async def fats_goal_chosen(message: types.Message, state: FSMContext):
    if not await is_positive_int(message.text):
        await message.answer(ENTER_POS_INT_MESSAGE)
        return
    await state.update_data(fats=int(message.text))
    user_data = await state.get_data()
    await edit_user_goals(message.from_user.id, user_data)
    await state.finish()
    await message.answer('Great! You have set all nutrition goals')


def register_goals_handlers(dp: Dispatcher):
    dp.register_message_handler(enter_calories_goal, commands='set_goals', state='*')
    dp.register_message_handler(calories_goal_chosen, state=SetGoal.waiting_for_calories_num)
    dp.register_message_handler(proteins_goal_chosen, state=SetGoal.waiting_for_proteins_num)
    dp.register_message_handler(carbs_goal_chosen, state=SetGoal.waiting_for_carbs_num)
    dp.register_message_handler(fats_goal_chosen, state=SetGoal.waiting_for_fats_num)
