import telebot
# from telebot import apihelper
import time



# proxies = {
#     'http': 'http://51.158.98.121:8811',
#     'https': 'http://51.158.98.121:8811',
# }

# apihelper.proxy = proxies
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def commnad_start_function(message):
    bot.reply_to(message, 'Рад Вас приветствовать!')


@bot.message_handler(commands=['admin'], func=lambda message: message.from_user.id == 209779127)
def admin(message):
    print(message)
    bot.reply_to(message, 'Хозяин, я рад тебя приветствовать!')


@bot.message_handler(commands=['admin_'])
def admin_(message):
    if (message.from_user.id == 109779127):
        bot.reply_to(message, 'Хозяин, я рад тебя приветствовать!')
    else:
        bot.reply_to(message, 'Ты не мой хозяин!')


@bot.message_handler(content_types=['text'])
def recieve_text(message):
    text = message.text
    bot.reply_to(message, f'Вы сказали:{text.upper()}')


# @bot.message_handler(content_types = ['text'])
# def recieve_text(message):
#     text = message.text
#     bot.reply_to(message, text[::-1])


bot.polling()
