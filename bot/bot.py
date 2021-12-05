#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

import telegram.error
from dotenv import load_dotenv, find_dotenv
import os

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    MessageHandler,
    Filters,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

bot = None
controller = None

# Map from user_id to chat_id with this user.
chats = dict()


def set_bot_controller(_controller):
    global controller
    controller = _controller


def start(update: Update, context: CallbackContext) -> int:
    if update is None or update.message is None or update.message.from_user is None:
        return
    player_id = update.message.from_user.id
    chats[player_id] = update.message.chat_id

    if controller.player_start(player_id):
        update.message.reply_text('Вы присоединились к игре')
    else:
        update.message.reply_text('Присоединиться не удалось\nВозможно, достигнуто максимальное количество игроков.\nПопробуйте позже.')


def on_message(update: Update, context: CallbackContext) -> int:
    if update is None or update.message is None:
        return
    user = update.message.from_user
    text = update.message.text
    logger.info("Message from %s: %s", user.id, text)
    controller.player_message(user.id, text)


# Buttons is list of strings. Each string represents one button.
def send_message(user_id, text, buttons=None):
    try:
        bot.send_message(chats[user_id], text)
    except telegram.error.TelegramError:
        logger.error("Failed to send message to " + str(user_id) + " " + text)


def bot_main() -> None:
    load_dotenv(find_dotenv())
    name = 'OD_BOT_TOKEN'
    my_token = os.environ.get(name)
    """Run the bot."""
    # Create the Updater and pass it your bot's token.

    updater = Updater(my_token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(Filters.regex(r'^/start$'), start))
    dispatcher.add_handler(MessageHandler(Filters.text, on_message))

    # Start the Bot
    updater.start_polling()

    # Set global bot
    global bot
    bot = updater.bot

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    bot_main()
