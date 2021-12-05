from quizclass import Quiz
from keyboard import Keyboard
from scoreboard import ScoreBoard
import telebot
from telebot import types
import datetime

__version__ = 0.0009


class QuizMain(object):
    def __init__(self):
        self.agents = dict()
        # ТОКЕН сделан хардкодом специально для тестов логин бота @help_me_start_bot
        self.bot = telebot.TeleBot('1292821995:AAH-tyF6p0opLx9vtX4W69iC2z30sln9O3U')
        self.message_to_send = str()
        self.button_row_idx = 0
        self.button_col_idx = 0
        self.sc = ScoreBoard()
        pass

    def main(self):
        @self.bot.message_handler(commands=['start', 'help', 'board', 'exit'])
        def process_start_command(message):
            print(message.text)

            hello_msg = "Привет, я Одиссей, чат-бот созданный для обучения кибербезопасности. " \
                        "Я помогу Вам защитится от троянов!\n" \
                        "Отвечайте на вопросы, а мы поможем вам улучшить ваши знания в этой области\n\n" \
                        "Для того чтобы вы могли начать сообщите свой контакт:"

            if message.text == '/start':
                self.agents.update({message.from_user.id: Quiz()})
                keyboard = Keyboard('Reply')
                keyboard.fill_kb_table([['Отправить контакт']], 'contact')
                self.bot.send_message(message.from_user.id, hello_msg, reply_markup=keyboard.get_instant())
                self.bot.register_next_step_handler(message, get_number)

            elif message.text == '/help':
                help_msg = "Доступные команды: \n" \
                            "/help - эта справка\n" \
                            "/start - начало работы с ботом \n" \
                            "/board - посмотреть статистику результатов \n" \
                            "/exit - прервать сессию."
                self.bot.send_message(message.from_user.id, help_msg)
            elif message.text == '/board':
                pass
            elif message.text == '/exit':
                if message.from_user.id in self.agents.keys():
                    self.agents[message.from_user.id].end_game_flag = True
                    self.end_of_the_game(message)
            pass

        def get_number(message):
            keyboard = Keyboard()

            """ For testing purpose """
            print('message', message.from_user.id)
            """ ------------------- """
            keyboard.fill_kb_table(self.agents[message.from_user.id].create_rows_cols_pic_box())
            self.bot.send_message(message.from_user.id, "Спасибо!", reply_markup=types.ReplyKeyboardRemove())
            self.bot.send_message(message.from_user.id, "Выберите вопрос:", reply_markup=keyboard.get_instant())
            self.agents[message.from_user.id].user_data.id = message.from_user.id
            self.agents[message.from_user.id].user_data.name = message.from_user.username

            self.agents[message.from_user.id].user_data.phone = message.json['contact']['phone_number']
            self.agents[message.from_user.id].user_data.time = datetime.datetime.now()

        @self.bot.callback_query_handler(func=lambda callback_data: True)
        def callback_worker(callback_data):
            print(callback_data.data)
            keyboard = Keyboard()
            print('callback', callback_data.from_user.id)
            keyboard.fill_kb_table(self.agents[callback_data.from_user.id].create_rows_cols_pic_box())
            if callback_data.data.startswith('table'):
                code = callback_data.data[-2:]
                print(code)
                if code.isdigit():
                    code = int(code)
                    self.button_row_idx = code // 10
                    self.button_col_idx = code % 10
                    if self.button_col_idx == 0:
                        return
                    show_question_and_answers(callback_data)
                self.bot.answer_callback_query(callback_data.id)
                pass
            elif callback_data.data.startswith('answer'):
                code = callback_data.data[-2:]
                print(code)
                if code.isdigit():
                    code = int(code)
                    button_num = code // 10
                is_answer_correct, user_answer_msg, correct_answer_msg, full_answer = self.agents[
                    callback_data.from_user.id].check_answer(button_num)
                full_answer = f"Справочная информация:\n{full_answer}"
                if is_answer_correct:
                    msg = f"Это правильный ответ! :\n" \
                          f"Ваш ответ: {user_answer_msg}\n" \
                          f"Правильный ответ: {correct_answer_msg}"
                    self.bot.send_message(callback_data.message.chat.id, msg)
                    self.bot.send_message(callback_data.message.chat.id, full_answer, reply_markup=keyboard.get_instant())
                else:
                    msg = f"Это неправильный ответ! :\n" \
                          f"Ваш ответ: {user_answer_msg}\n" \
                          f"Правильный ответ: {correct_answer_msg}"
                    self.bot.send_message(callback_data.message.chat.id, msg)
                    self.bot.send_message(callback_data.message.chat.id, full_answer, reply_markup=keyboard.get_instant())
                if self.agents[callback_data.from_user.id].end_game_flag:
                    self.end_of_the_game(callback_data)

        def show_question_and_answers(callback_data):
            question_msg, answers_list = self.agents[callback_data.from_user.id].get_question_and_answers(
                self.button_row_idx, self.button_col_idx - 1)
            print(answers_list)
            kb = Keyboard()
            kb.fill_kb_table(answers_list, table_type='answer')
            self.bot.send_message(callback_data.message.chat.id,
                    f"Вопрос №{self.agents[callback_data.message.chat.id].questions_count}\n{question_msg}",
                    reply_markup=kb.get_instant())
            pass
        self.bot.polling(none_stop=True, interval=0)
        pass

    def end_of_the_game(self, message):
        msg = "Поздравляем!\n"
        count_questions_in_game = self.agents[message.from_user.id].q_a_matrix_rows * self.agents[
            message.from_user.id].q_a_matrix_cols
        if self.agents[message.from_user.id].questions_count == count_questions_in_game:
            msg += "Вы ответили на все вопросы в игре!\n"
        else:
            msg += f"Вы ответили на {self.agents[message.from_user.id].questions_count} из {count_questions_in_game} вопросов!\n" \
                   "Чтобы набрать больше баллов отвечайте на все вопросы.\n"
        msg += f"Ваш результат в игре: {self.agents[message.from_user.id].user_score} очков"
        self.bot.send_message(message.from_user.id, msg)
        time_elapsed = datetime.datetime.now() - self.agents[message.from_user.id].user_data.time
        self.agents[message.from_user.id].user_data.time = str(time_elapsed)
        self.agents[message.from_user.id].user_data.score = self.agents[message.from_user.id].user_score
        """ Warning! Save user data before delete """
        self.sc.add_data(self.agents[message.from_user.id].user_data)
        self.sc.save_data()
        self.agents.pop(message.from_user.id)
        pass


if __name__ == "__main__":
    quiz = QuizMain()
    quiz.main()
