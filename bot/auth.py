import logging

from telegram import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    Update)

from telegram.ext import (MessageHandler, Filters)

import bot.bot

NO_RIGHTS, DENIED, PLAY_RIGHTS, ADMIN_RIGHTS = range(4)
rights_text = {NO_RIGHTS: "не определено",
               DENIED: "нет доступа",
               PLAY_RIGHTS: "игрок",
               ADMIN_RIGHTS: "администратор"}


class Auth:
    def __init__(self):
        self.access_rights = dict()
        self.phone_handler = MessageHandler(Filters.contact, self.phone_given)

    def get_rights(self, user_id):
        if user_id in self.access_rights:
            return self.access_rights[user_id]
        return NO_RIGHTS

    def register(self, update):
        bot.bot.updater.dispatcher.add_handler(self.phone_handler)
        update.message.reply_text(
            'Необходимо зарегистрироваться. Передайте ваш номер телефона.',
            reply_markup=ReplyKeyboardMarkup(
                [[KeyboardButton("Продолжить с номером телефона", request_contact=True)]],
                one_time_keyboard=False),
            disable_web_page_preview=True
        )

    def phone_given(self, update, c):
        bot.bot.updater.dispatcher.remove_handler(self.phone_handler)
        contact = update.message.contact
        if contact is None:
            return
        phone_number = contact.phone_number.replace('+', '')
        logging.info("Got user phone: " + phone_number)
        level = PLAY_RIGHTS
        self.access_rights[contact.user_id] = level

        if level > DENIED:
            update.message.reply_text(
                'Ваш доступ: ' + rights_text[level] + ", нажмите для продолжения: /start")

    def authorize(self, update: Update):
        user_id = update.message.from_user.id

        if NO_RIGHTS == self.get_rights(user_id):
            self.register(update)
            # No registration yet
            return False
        # Registration complete
        return True
