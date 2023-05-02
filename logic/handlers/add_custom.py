from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from logic.data_handlers.database_manager import edit_user_macros
from logic.data_handlers.valid_checker import is_positive_int
from resources.messages import ENTER_POS_INT_MESSAGE, added_meal_message


class Meal(StatesGroup):
    waiting_for_calories = State()
    waiting_for_grams = State()
    waiting_for_proteins = State()
    waiting_for_carbs = State()
    waiting_for_fats = State()


async def enter_calories(message: types.Message, state: FSMContext):
    await message.answer('Please, enter meal calories below:')
    await state.set_state(Meal.waiting_for_calories.state)


async def calories_chosen(message: types.Message, state: FSMContext):
    if not await is_positive_int(message.text):
        await message.answer(ENTER_POS_INT_MESSAGE)
        return
    await state.update_data(calories=int(message.text))
    await state.set_state(Meal.waiting_for_proteins.state)
    await message.answer('Great! Next step - enter meal grams of proteins:')


async def proteins_chosen(message: types.Message, state: FSMContext):
    if not await is_positive_int(message.text):
        await message.answer(ENTER_POS_INT_MESSAGE)
        return
    await state.update_data(protein_g=int(message.text))
    await state.set_state(Meal.waiting_for_carbs.state)
    await message.answer('Great! Next step - enter meal grams of carbs:')


async def carbs_chosen(message: types.Message, state: FSMContext):
    if not await is_positive_int(message.text):
        await message.answer(ENTER_POS_INT_MESSAGE)
        return
    await state.update_data(carbohydrates_total_g=int(message.text))
    await state.set_state(Meal.waiting_for_fats.state)
    await message.answer('Great! Next step - enter meal grams of fats:')


async def fats_chosen(message: types.Message, state: FSMContext):
    if not await is_positive_int(message.text):
        await message.answer(ENTER_POS_INT_MESSAGE)
        return
    await state.update_data(fat_total_g=int(message.text))
    data = await state.get_data()
    await edit_user_macros(message.from_user.id, data)
    await state.finish()
    await message.answer(await added_meal_message(data))


def register_add_custom_handlers(dp: Dispatcher):
    dp.register_message_handler(enter_calories, commands='add_custom', state='*')
    dp.register_message_handler(calories_chosen, state=Meal.waiting_for_calories)
    dp.register_message_handler(proteins_chosen, state=Meal.waiting_for_proteins)
    dp.register_message_handler(carbs_chosen, state=Meal.waiting_for_carbs)
    dp.register_message_handler(fats_chosen, state=Meal.waiting_for_fats)
