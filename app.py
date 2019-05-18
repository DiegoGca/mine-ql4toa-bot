#!/usr/bin/env python3

from telegram.ext import Updater
from telegram.ext import CommandHandler

from credentials import (TOKEN, LIST_OF_ADMINS, MSPORT, MSURL)

import statusping

updater = Updater(token=TOKEN, use_context=True)
dp = updater.dispatcher


def start(update, context):
    print("Holaa")
    context.bot.send_message(chat_id=update.message.chat_id,
        text="Hola!")


def raw(update, context):
    sp = statusping.StatusPing(MSURL, MSPORT, 10)
    text = sp.get_status()
    print(text)
    context.bot.send_message(chat_id=update.message.chat_id,
        text=text)


start_handler = CommandHandler('start', start)
dp.add_handler(start_handler)
raw_handler = CommandHandler('raw', raw)
dp.add_handler(raw_handler)


updater.start_polling()
