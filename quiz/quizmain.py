from keyboard import Keyboard
from quizclass import Quiz
# from game.player import Player
import telebot
from telebot import types

__version__ = 0.0001


class QuizMain(object):
    def __init__(self):
        self.quiz = Quiz()
        self.keyboard = Keyboard()
        self.bot = telebot.TeleBot('1292821995:AAH-tyF6p0opLx9vtX4W69iC2z30sln9O3U');
        data_str, _  = self.quiz.create_rows_cols_pic_box()
        self.keyboard.fill_kb_table(data_str)
        # self.keyboard.fill_kb_table([['Тема 1', 100, 200, 300, 400],
        #                             ['Тема 2', 100, 200, 300, 400],
        #                             ['Тема 3', 100, 200, 300, 400],
        #                             ['Тема 4', 100, 200, 300, 400],
        #                             ['Тема 5', 100, 200, 300, 400]])
        pass

    def main(self):
        @self.bot.callback_query_handler(func=lambda callback_data: True)
        def callback_worker(callback_data):
            print(callback_data.data)
            code = callback_data.data[-2]
            if code.isdigit():
                code = int(code)
                row = code // 10
                col = code % 10
            self.bot.answer_callback_query(callback_data.id)
            pass

        @self.bot.message_handler(commands=['start', 'rm'])
        def process_start_command(message):
            print(message.text)
            if message.text == '/start':
                self.bot.send_message(message.from_user.id, "start", reply_markup=self.keyboard.get_instant())
            if message.text == '/rm':
                self.bot.send_message(message.from_user.id, "rm", reply_markup=types.ReplyKeyboardRemove())
            pass
        pass

        self.bot.polling(none_stop=True, interval=0)

        pass

if __name__ == "__main__":
    quiz = QuizMain()
    quiz.main()
