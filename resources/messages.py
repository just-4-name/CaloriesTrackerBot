from logic.data_handlers.formatter import format_data

HELP_MESSAGE = 'My commands are:' \
               '\n/start - start bot' \
               '\n/set_goals - set your nutrition goals' \
               '\n/add - add meal to today macros' \
               '\n/today - learn macros for today' \
               '\n/achieved - learn your achievements for today' \
               '\n/new_day - start new day (annul all macros)' \
               '\n/add_custom add custom meal and enter its macros' \
               '\n/cancel - cancel currently running command' \
               '\n/help - help'

ENTER_POS_INT_MESSAGE = 'Oops, please, enter positive integer number'
NEW_DAY_MESSAGE = 'Great! Started new day, continue sticking to your nutrition plan!'
ASK_ENTER_GOALS_MESSAGE = "Oops, set your nutrition goals first with /set_goals command"
NO_SUCH_MEAL_MESSAGE = "Oops, unfortunately, I don't know such meal. Please, check for typos or enter macros " \
                       "from the Internet"


async def hello_message(name):
    return f"Hello, {name}!\nI am calories tracking bot!\n{HELP_MESSAGE}"


async def added_meal_message(data):
    return f"You have added new meal of:{await format_data(data)}"
