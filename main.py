from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher

import data_base
import keyboard

TOKEN = ''
TelegramBot = Bot(token=TOKEN)
dp = Dispatcher(TelegramBot)
db = data_base


@dp.message_handler(commands=['start', 'начать'])
async def start(msg: types.Message):
    array = []
    for i in range(len(db.Stage.query.all())):
        try:
            array.append(db.Stage.query.all()[i].chat_id)
        except:
            continue
    if msg.chat.id in array:
        check = True
    else:
        check = False
    if check is False:
        await msg.answer(text="Привет!", reply_markup=keyboard.main_menu())
        # data_base.stage(chat_id=msg.chat.id, stage="start")
    else:
        await msg.answer(text="Привет!", reply_markup=keyboard.main_menu())


@dp.message_handler(content_types=['text'])
async def send_answer(msg: types.Message):
    if msg.text == "Задать вопрос":
        await msg.answer(text="Категории", reply_markup=keyboard.all_questions_answer(data="questions"))
    if msg.text == "Ответить на вопросы":
        await msg.answer(text="Категории", reply_markup=keyboard.all_questions_answer(data="answers"))
    if msg.text == "Мои вопросы":
        await msg.answer(text="Вопросы", reply_markup=keyboard.my_questions())
    if msg.text == "Мои ответы":
        await msg.answer(text="Ваши ответы", reply_markup=keyboard.my_answer())
    if msg.text == "Фоурм":
        await msg.answer(text="Фоурм", reply_markup=keyboard.all_questions_answer(data="fourm"))

course_n = None
subject_n = None
valid_subject = {"course": course_n, "subject": subject_n}
subject_array_selected = []





if __name__ == '__main__':
    executor.start_polling(dp)
