import configparser

from discord_bot.main_bot import bot
from flask_route import run_flask

config = configparser.ConfigParser()
config.read('setting/botToken.ini')

botToken = config['setting']['botToken']

if __name__ == '__main__':
    # flask_thread = threading.Thread(target=run_flask)
    # flask_thread.start()

    bot.run(botToken)