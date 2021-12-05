import logging

from telegram import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update)

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

import bot.bot

NO_RIGHTS, DENIED, PLAY_RIGHTS, ADMIN_RIGHTS = range(4)


class Auth:
    def __init__(self):
        self.access_rights = dict()

    def get_rights(self, user_id):
        return NO_RIGHTS

    def register(self, update):
        bot.bot.updater.dispatcher.add_handler(MessageHandler(Filters.contact, self.phone_given))
        update.message.reply_text(
            'Необходимо зарегистрироваться. Передайте ваш номер телефона.',
            reply_markup=ReplyKeyboardMarkup(
                [[KeyboardButton("Продолжить с номером телефона", request_contact=True)]],
                one_time_keyboard=False),
            disable_web_page_preview=True
        )

    def phone_given(self, update, c):
        contact = update.message.contact

        if contact is None:
            return ConversationHandler.END

        phone_number = contact.phone_number.replace('+', '')

        logging.info("Got user phone: " + phone_number)

        level = PLAY_RIGHTS

        update.message.reply_text(
            'Ваш доступ: ' + str(level),
            reply_markup=ReplyKeyboardRemove, one_time_keyboard=False)

    def authorize(self, update: Update):
        user_id = update.message.from_user.id

        if NO_RIGHTS == self.get_rights(user_id):
            self.register(update)
