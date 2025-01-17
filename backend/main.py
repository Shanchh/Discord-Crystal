import threading

from discord_bot.main_bot import bot
from flask_route import app
from setting.token import botToken

def run_flask():
    app.run(host="127.0.0.1", port=6620)

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    bot.run(botToken)