With this telegram bot you can:
- Set daily calories and macros goals
- Add meals by entering meal name and number of grams (data is fetched from this site API: https://api-ninjas.com/api/nutrition)
- Add custom meals by entering number of calories and macros
- Check if your goals are reached

Data is stored via sqlite3 using this library: https://github.com/omnilib/aiosqlite (it provides async interfase for sqlite3)

How to run project:
- Clone repository
- pip install -r requirements.txt
- set token variable in config/bot.ini file 
- python3 bot.py
- open bot in telegram 
- enter /start command

with /help command you can get list of all bot commands with brief description, and it is also given in message after /start command.
