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
        self.message_to_send = str()
        self.button_row_idx = 0
        self.button_col_idx = 0

        # self.bot_logic_initialization()
        pass

    def main(self):
        """ 1. init bot logic """
        data_str, _ = self.quiz.create_rows_cols_pic_box()
        self.keyboard.fill_kb_table(data_str)

        @self.bot.message_handler(commands=['start', 'rm'])
        def process_start_command(message):
            print(message.text)
            hello_msg = "Привет, я Одиссей, чат-бот созданный для обучения кибербезопасности. " \
                        "Мой тёзка придумал Троянского коня, а я помогу Вам защитится от троянов!\n" \
                        "Отвечайте на вопросы, а мы поможем вам улучшить ваши знания в этой области"

            if message.text == '/start':
                self.bot.send_message(message.from_user.id, hello_msg, reply_markup=self.keyboard.get_instant())
            if message.text == '/rm':
                self.bot.send_message(message.from_user.id, "rm", reply_markup=types.ReplyKeyboardRemove())
            pass

        @self.bot.callback_query_handler(func=lambda callback_data: True)
        def callback_worker(callback_data):
            print(callback_data.data)
            code = callback_data.data[-2]
            if code.isdigit():
                code = int(code)
                self.button_row_idx = code // 10
                self.button_col_idx = code % 10
                show_question_and_answers(callback_data)
            self.bot.answer_callback_query(callback_data.id)
            pass
        # bot.register_next_step_handler(message, get_name)

        def show_question_and_answers(callback_data):
            question_msg, answers_list = self.quiz.get_question_and_answers(self.button_row_idx, self.button_col_idx)
            self.bot.send_message(callback_data.message.chat.id, question_msg)
            # self.bot.register_next_step_handler(question_msg, get_name)
            pass

        self.bot.polling(none_stop=True, interval=0)
        pass


if __name__ == "__main__":
    quiz = QuizMain()
    quiz.main()
