
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.utils.markdown import text
from aiogram.dispatcher import Dispatcher

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton




class Keyboard(object):
    def __init__(self):
        self.kb_table = ReplyKeyboardMarkup(resize_keyboard=True)
        pass

    def fill_kb_table(self, table):
        i = 0
        for row in table:
            buttons = []
            j = 0
            for cell in row:
                buttons.append(InlineKeyboardButton(f'{cell}', callback_data=f'btn{i}{j}'))
                j += 1
            self.kb_table.keyboard.append(buttons)
            i += 1
        pass

    def get_instant(self):
        return self.kb_table


def main():
    bot = Bot(token='1292821995:AAH-tyF6p0opLx9vtX4W69iC2z30sln9O3U')
    dp = Dispatcher(bot)
    keyboard = Keyboard()
    keyboard.fill_kb_table([['Тема 1', 100, 200, 300, 400],
                            ['Тема 2', 100, 200, 300, 400],
                            ['Тема 3', 100, 200, 300, 400],
                            ['Тема 4', 100, 200, 300, 400],
                            ['Тема 5', 100, 200, 300, 400]])

    @dp.message_handler(commands=['start'])
    async def process_start_command(message: types.Message):
        await message.reply("Первая инлайн кнопка", reply_markup=keyboard.get_instant())

    @dp.message_handler(commands=['rm'])
    async def process_rm_command(message: types.Message):
        await message.reply("Убираем шаблоны сообщений", reply_markup=ReplyKeyboardRemove())

    @dp.callback_query_handler(func=lambda c: c.data and c.data.startswith('btn'))
    async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
        code = callback_query.data[-1]
        if code.isdigit():
            code = int(code)
        if code == 2:
            await bot.answer_callback_query(callback_query.id, text='Нажата вторая кнопка')
        elif code == 5:
            await bot.answer_callback_query(
                callback_query.id,
                text='Нажата кнопка с номером 5.\nА этот текст может быть длиной до 200 символов 😉', show_alert=True)
        else:
            await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, f'Нажата инлайн кнопка! code={code}')

    @dp.callback_query_handler(func=lambda c: c.data and c.data.startswith('btn'))
    async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
        code = callback_query.data[-2]
        if code.isdigit():
            code = int(code)
            row = code // 10
            col = code % 10

        await bot.answer_callback_query(callback_query.id)


    executor.start_polling(dp)


if __name__ == "__main__":
    main()
