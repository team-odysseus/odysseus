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

# Map from user_id to chat_id with this user.
chats = dict()


def start(update: Update, context: CallbackContext) -> int:
    if update is None or update.message is None or update.message.from_user is None:
        return
    chats[update.message.from_user.id] = update.message.chat_id
    update.message.reply_text('Game started')


def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )


def on_text(update: Update, context: CallbackContext) -> int:
    if update is None or update.message is None:
        return
    user = update.message.from_user
    text = update.message.text
    logger.info("Message from %s: %s", user.id, text)
    update.message.reply_text('Thank you!')
    for chat_id in chats.values():
        if chat_id != chats[user.id]:
            send_message(chat_id, text, ["Yes", "No"])
            logger.info("Sent message to " + str(chat_id))


# Buttons is list of strings. Each string represents one button.
def send_message(user_id, text, buttons=None):
    try:
        bot.send_message(chats[user_id], text)
    except telegram.error.TelegramError:
        logger.error("Failed to send message to " + str(user_id) + " " + text)


def main() -> None:
    load_dotenv(find_dotenv())
    name = 'OD_BOT_TOKEN'
    my_token = os.environ.get(name)
    """Run the bot."""
    # Create the Updater and pass it your bot's token.

    updater = Updater(my_token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(Filters.regex(r'^/start$'), start))
    dispatcher.add_handler(MessageHandler(Filters.text, on_text))

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
    main()
