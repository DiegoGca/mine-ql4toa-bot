#!/usr/bin/env python3
import os
import sys
import logging

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram import ChatAction

from functools import wraps

import statusping

# Enabling logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

#######
try:
    from credentials import (TOKEN, LIST_OF_ADMINS, MODE, MSPORT, MSURL)
except (ImportError, ModuleNotFoundError):
    TOKEN = os.getenv('TOKEN')
    MODE = os.getenv('MODE', 'dev')
    MSPORT = int(os.getenv('MSPORT'))
    MSURL = os.getenv('MSURL')

#######
mode = MODE

logging.info('Starting bot...%s', mode)
if mode == "dev":
    def run(updater):
        updater.start_polling()
elif mode == "prod":
    def run(updater):
        PORT = int(os.environ.get("PORT", "8443"))
        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
        # Code from https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks#heroku
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN)
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))
else:
    print(mode)
    logger.error("No MODE specified!")
    sys.exit(1)

#######
def send_action(action):
    """Sends typing action while processing func command."""

    def decorator(func):
        @wraps(func)
        def command_func(update, context, *args, **kwargs):
            context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return func(update, context,  *args, **kwargs)

        return command_func
    return decorator


########
def p_online(players):
    text = "Jugadores online: "
    online = players['online']
    max = players['max']
    jugadores = ""
    for p in players['sample']:
        jugadores += " - " + p['name']

    text += str(online) + "/" + str(max) + "\n"
    text += jugadores

    return text


def serv_info(serv):
    text = "QL4TOA MINECRAFT SERVER\n" +\
    "——————————————\n" + \
    "Server Status: " + \
    "ONLINE\n"

    text += "url: "+ MSURL + ":" + str(MSPORT) + "\n"
    text += "version: " + serv['version']['name'] + "\n"
    text += "ping: " + str(serv['ping'])

    return text

########

def start(update, context):
    print("Holaa")
    context.bot.send_message(chat_id=update.message.chat_id,
        text="Hola!")


@send_action(ChatAction.TYPING)
def raw(update, context):
    sp = statusping.StatusPing(MSURL, MSPORT, 10)
    text = sp.get_status()
    context.bot.send_message(chat_id=update.message.chat_id,
        text=text)


@send_action(ChatAction.TYPING)
def players(update, context):
    sp = statusping.StatusPing(MSURL, MSPORT, 10)
    text = sp.get_status()
    text = p_online(text['players'])
    context.bot.send_message(chat_id=update.message.chat_id,
        text=text)


@send_action(ChatAction.TYPING)
def get_serv_info(update, context):
    sp = statusping.StatusPing(MSURL, MSPORT, 10)
    raw = sp.get_status()

    text = serv_info(raw)
    context.bot.send_message(chat_id=update.message.chat_id,
        text=text)


@send_action(ChatAction.TYPING)
def get_serv_status(update, context):
    sp = statusping.StatusPing(MSURL, MSPORT, 10)
    raw = sp.get_status()
    info = serv_info(raw)
    players = p_online(raw['players'])
    text = info + "\n" + players
    context.bot.send_message(chat_id=update.message.chat_id,
        text=text)


if __name__ == '__main__':
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dp.add_handler(start_handler)
    raw_handler = CommandHandler('raw', raw)
    dp.add_handler(raw_handler)
    raw_handler = CommandHandler(['players', 'gente', 'jugadores', 'p'], players)
    dp.add_handler(raw_handler)
    raw_handler = CommandHandler('server', get_serv_info)
    dp.add_handler(raw_handler)
    raw_handler = CommandHandler('status', get_serv_status)
    dp.add_handler(raw_handler)

    run(updater)
