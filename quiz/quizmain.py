import os
import time
import logging
import threading
import datetime
import telebot
import telebot.apihelper
from telebot import types

from quizclass import Quiz
from keyboard import Keyboard
from scoreboard import ScoreBoard


__version__ = 0.0015

STORAGE_PATH = os.getcwd()
log_filepath = os.path.join(STORAGE_PATH, 'log.log')

class QuizMain(object):
    def __init__(self):
        self.agents = dict()
        # ТОКЕН сделан хардкодом специально для тестов логин бота @help_me_start_bot
        self.bot = telebot.TeleBot('1292821995:AAH-tyF6p0opLx9vtX4W69iC2z30sln9O3U')
        self.message_to_send = str()
        self.button_row_idx = 0
        self.button_col_idx = 0
        self.scoreboard = ScoreBoard()
        self.hello_msg = "Привет, я Одиссей, чат-бот созданный для обучения кибербезопасности. " \
                         "Я помогу Вам защитится от троянов!\n" \
                         "Отвечайте на вопросы, а мы поможем вам улучшить ваши знания в этой области\n\n" \
                         "Для того чтобы вы могли начать сообщите свой контакт нажав на кноку внизу "
        self.logger = self.get_logger()
        self.watchdog_timer = 60
        self.watchdog = threading.Thread(target=self.watchdog_envelope(),
                                         name="inactivity_watchdog",
                                         args=(15, self.logger),
                                         # daemon=True
                                         )

        pass

    @staticmethod
    def get_logger():
        logger = logging.getLogger("bot log")
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(log_filepath)
        fmt = '%(asctime)s - %(threadName)s - %(levelname)s - %(message)s'
        formatter = logging.Formatter(fmt)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        return logger

    def inactivity_watchdog(self):
        self.logger.info(f'MSG : inactivity timeout -> start checking')
        for user_id in self.agents.keys():
            inactivity_treshold = self.agents[user_id].user_data.last_user_activity + self.agents[
                user_id].user_data.user_activity_treshhold
            if inactivity_treshold < datetime.datetime.now():
                msg = f"Ввиду отсутствия вас в игре более {self.agents[user_id].user_data.user_activity_treshhold} минут," \
                      f"\n игра закончена. Ознакомьтесь с вашим результатом!\n"
                msg += f"{self.end_of_game_score(user_id)}"
                self.logger.info(f'MSG : {user_id} : inactivity timeout')
                self.end_of_the_game(self.agents[user_id].last_callback)
            else:
                self.logger.info(f'MSG : {user_id} inactivity timeout -> ok')
        pass

    def watchdog_envelope(self):
        while True:
            self.inactivity_watchdog()
            time.sleep(self.watchdog_timer)
        pass

    def main(self):
        @self.bot.message_handler(commands=['start', 'help', 'board', 'exit'])
        def process_start_command(message):

            """ Logging """
            self.logger.info(f'MSG : {message.from_user.id} : {message.text}')

            if message.text == '/start':
                if not (message.from_user.id in self.agents):
                    self.agents.update({message.from_user.id: Quiz()})
                    keyboard = Keyboard('Reply')
                    keyboard.fill_kb_table([['Отправить контакт']], 'contact')
                    self.bot.send_message(message.from_user.id, self.hello_msg, reply_markup=keyboard.get_instant())
                    self.bot.register_next_step_handler(message, get_number)
                else:
                    self.bot.send_message(message.from_user.id,
                                          'Прежде чем начать заново закончите текущую сессию /exit')
                    return
            elif message.text == '/help':
                help_msg = "Доступные команды: \n" \
                           "/help - эта справка\n" \
                           "/start - начало работы с ботом \n" \
                           "/board - посмотреть статистику результатов \n" \
                           "/exit - прервать сессию."
                self.bot.send_message(message.from_user.id, help_msg)
            elif message.text == '/board':
                score_msg = self.scoreboard.get_hiscore()
                self.bot.send_message(message.from_user.id, score_msg)

                """ Save last activity time and callback/message """
                self.agents[message.from_user.id].user_data.last_user_activity = datetime.datetime.now()
                self.agents[message.from_user.id].user_data.last_callback = message

            elif message.text == '/exit':
                if message.from_user.id in self.agents.keys():
                    self.agents[message.from_user.id].end_game_flag = True
                    """ Save last activity time and callback/message """
                    self.agents[message.from_user.id].user_data.last_user_activity = datetime.datetime.now()
                    self.agents[message.from_user.id].user_data.last_callback = message
                    self.end_of_the_game(message)

            pass

        def get_number(message):
            """ Logging """
            self.logger.info(f'MSG : {message.from_user.id} : {message.text}')

            if message.text is not None:
                keyboard = Keyboard('Reply')
                keyboard.fill_kb_table([['Отправить контакт']], 'contact')
                self.bot.send_message(message.from_user.id, "Нужно нажать на кнопку и подтвердить передачу контакта.")
                self.bot.send_message(message.from_user.id, self.hello_msg, reply_markup=keyboard.get_instant())
                self.bot.register_next_step_handler(message, get_number)
            else:
                keyboard = Keyboard()
                keyboard.fill_kb_table(self.agents[message.from_user.id].create_rows_cols_pic_box())
                self.bot.send_message(message.from_user.id, "Спасибо!", reply_markup=types.ReplyKeyboardRemove())
                self.bot.send_message(message.from_user.id, "Выберите вопрос:", reply_markup=keyboard.get_instant())
                self.agents[message.from_user.id].user_data.id = message.from_user.id
                self.agents[message.from_user.id].user_data.name = message.from_user.username
                self.agents[message.from_user.id].status = 1
                self.agents[message.from_user.id].user_data.phone = message.json['contact']['phone_number']
                self.agents[message.from_user.id].user_data.time = datetime.datetime.now()

                """ Save last activity time and callback/message """
                self.agents[message.from_user.id].user_data.last_user_activity = datetime.datetime.now()
                self.agents[message.from_user.id].user_data.last_callback = message
                pass

        @self.bot.callback_query_handler(func=lambda callback_data: True)
        def callback_worker(callback_data):
            """ Logging """
            self.logger.info(f'CALLBACK : {callback_data.from_user.id} : {callback_data.data}')
            if callback_data.from_user.id not in self.agents:
                self.bot.send_message(callback_data.message.chat.id, "Начните с /start  !")
                return

            if callback_data.data.startswith('table'):
                """ Save last activity time """
                self.agents[callback_data.from_user.id].user_data.last_user_activity = datetime.datetime.now()
                if self.agents[callback_data.from_user.id].status != 1:
                    self.bot.send_message(callback_data.message.chat.id, "Выберите ответ на вопрос!")
                    return
                code = callback_data.data[-2:]
                if code.isdigit():
                    code = int(code)
                    self.button_row_idx = code // 10
                    self.button_col_idx = code % 10
                    if self.button_col_idx == 0:
                        return
                    self.agents[callback_data.from_user.id].status = 2
                    show_question_and_answers(callback_data)
                self.bot.answer_callback_query(callback_data.id)
            elif callback_data.data.startswith('answer'):
                if self.agents[callback_data.from_user.id].status != 2:
                    self.bot.send_message(callback_data.message.chat.id, "Выберите категорию и цену вопроса!")
                    return
                keyboard = Keyboard()
                keyboard.fill_kb_table(self.agents[callback_data.from_user.id].create_rows_cols_pic_box())
                code = callback_data.data[-2:]
                if code.isdigit():
                    code = int(code)
                    button_num = code // 10
                is_answer_correct, user_answer_msg, correct_answer_msg, full_answer = self.agents[
                    callback_data.from_user.id].check_answer(button_num)
                full_answer = f"Справочная информация:\n{full_answer} \n\n" \
                              "/help - для справки по командам"
                if is_answer_correct:
                    msg = f"Это правильный ответ! :\n" \
                          f"Ваш ответ: {user_answer_msg}\n" \
                          f"Правильный ответ: {correct_answer_msg}"
                    self.bot.send_message(callback_data.message.chat.id, msg)
                    self.bot.send_message(callback_data.message.chat.id, full_answer,
                                          reply_markup=keyboard.get_instant())
                else:
                    msg = f"Это неправильный ответ! :\n" \
                          f"Ваш ответ: {user_answer_msg}\n" \
                          f"Правильный ответ: {correct_answer_msg}"
                    self.bot.send_message(callback_data.message.chat.id, msg)
                    self.bot.send_message(callback_data.message.chat.id, full_answer,
                                          reply_markup=keyboard.get_instant())
                self.agents[callback_data.from_user.id].status = 1
                if self.agents[callback_data.from_user.id].end_game_flag:
                    self.end_of_the_game(callback_data)
            pass

        def show_question_and_answers(callback_data):
            question_msg, answers_list = self.agents[callback_data.from_user.id].get_question_and_answers(
                self.button_row_idx, self.button_col_idx - 1)
            kb = Keyboard()
            kb.fill_kb_table(answers_list, table_type='answer')
            self.bot.send_message(callback_data.message.chat.id,
                                  f"Вопрос №{self.agents[callback_data.message.chat.id].questions_count}\n{question_msg}",
                                  reply_markup=kb.get_instant())
            pass
        self.watchdog.start()
        self.bot.polling(none_stop=True, interval=1)
        pass

    def end_of_game_score(self, user_id):
        msg = str()
        count_questions_in_game = self.agents[user_id].q_a_matrix_rows * self.agents[user_id].q_a_matrix_cols
        if self.agents[user_id].questions_count == count_questions_in_game:
            msg += "Вы ответили на все вопросы в игре!\n"
        else:
            msg += f"Вы ответили на {self.agents[user_id].questions_count} из {count_questions_in_game} вопросов!\n" \
                   "Чтобы набрать больше баллов отвечайте на все вопросы.\n"
        msg += f"Ваш результат в игре: {self.agents[user_id].user_score} очков"

        """ Logging """
        self.logger.info(f'END_OF_GAME : {user_id} : score = {self.agents[user_id].user_score}')
        return msg

    def end_of_the_game(self, message):
        msg = "Поздравляем!\n"
        msg += f"{self.end_of_game_score(message.from_user.id)}"

        self.bot.send_message(message.from_user.id, msg)
        time_elapsed = datetime.datetime.now() - self.agents[message.from_user.id].user_data.time
        self.agents[message.from_user.id].user_data.time = str(time_elapsed)
        self.agents[message.from_user.id].user_data.score = self.agents[message.from_user.id].user_score

        """ Warning! Save user data before delete """
        self.scoreboard.add_data(self.agents[message.from_user.id].user_data)
        self.scoreboard.save_data()
        self.agents.pop(message.from_user.id)
        pass


if __name__ == "__main__":
    quiz = QuizMain()
    quiz.main()
