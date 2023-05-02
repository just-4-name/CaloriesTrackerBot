from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from logic.data_handlers.database_manager import edit_user_macros
from logic.data_handlers.site_parser import FoodSearcher
from logic.data_handlers.valid_checker import is_positive_int
from resources.messages import ENTER_POS_INT_MESSAGE, NO_SUCH_MEAL_MESSAGE, added_meal_message


class Meal(StatesGroup):
    waiting_for_name = State()
    waiting_for_grams = State()


async def enter_meal_name(message: types.Message, state: FSMContext):
    await message.answer('Please, enter meal name below:')
    await state.set_state(Meal.waiting_for_name.state)


async def meal_name_chosen(message: types.Message, state: FSMContext, food_searcher: FoodSearcher):
    if not await food_searcher.check_if_in_db(message.text.lower()):
        await message.answer(NO_SUCH_MEAL_MESSAGE)
        return
    await state.update_data(name=message.text.lower())
    await state.set_state(Meal.waiting_for_grams.state)
    await message.answer('Great! Next step - enter number of grams:')


async def grams_num_chosen(message: types.Message, state: FSMContext, food_searcher: FoodSearcher):
    if not await is_positive_int(message.text):
        await message.answer(ENTER_POS_INT_MESSAGE)
        return
    state_data = await state.get_data()
    data = await food_searcher.search_food(state_data["name"], int(message.text))
    await edit_user_macros(message.from_user.id, data)
    await state.finish()
    await message.answer(await added_meal_message(data))


def register_add_meal_handlers(dp: Dispatcher):
    dp.register_message_handler(enter_meal_name, commands='add', state='*')
    dp.register_message_handler(meal_name_chosen, state=Meal.waiting_for_name)
    dp.register_message_handler(grams_num_chosen, state=Meal.waiting_for_grams)
