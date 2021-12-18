from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher

import data_base
import keyboard

TOKEN = '2074633156:AAFx1hqXASCnjtXBC1_FDFGhJp8pIOmPZW4'
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


@dp.callback_query_handler(text_contains=['status_'])
async def status(call: types.CallbackQuery):
    if call.data and call.data.startswith("status_"):
        data = call.data.split("_")[1]
        code = "test"
        message_menu = 'Выберите предметы, которые вы ведете.' \
                       ' По заверешению, нажмите кнопку "подтвердить"'
        message_status = "Статус сохранен"

        if data == "back":
            db.delete_stage(chat_id=call.from_user.id)
            data_base.stage(chat_id=call.from_user.id, stage="start")
            await dp.bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
            await dp.bot.send_message(chat_id=call.from_user.id,
                                      text="Выберите статус",
                                      reply_markup=keyboard.choose_status())

        if data == "back-menu":
            valid_subject["course"] = None
            db.delete_stage(chat_id=call.from_user.id)
            db.stage(chat_id=call.from_user.id, stage="choose_course")
            await dp.bot.delete_message(chat_id=call.from_user.id,
                                        message_id=call.message.message_id)
            await dp.bot.send_message(chat_id=call.from_user.id,
                                      text=message_menu,
                                      reply_markup=keyboard.choose_course())

        if data == "teacher":
            await dp.bot.send_message(chat_id=call.from_user.id, text="Введите пароль преподавателя")
            try:
                if db.Stage.query.filter_by(chat_id=call.from_user.id).all()[0] is not None:
                    db.delete_stage(chat_id=call.from_user.id)
            except:
                pass
            db.stage(chat_id=call.from_user.id, stage="login")


        array_course = [1, 2, 3, 4]
        for course in array_course:
            try:
                if course == int(data):
                    valid_subject["course"] = course
                    await call.answer("Курс выбран")
                    await dp.bot.edit_message_text(chat_id=call.from_user.id,
                                                   message_id=call.message.message_id,
                                                   text=message_menu,
                                                   reply_markup=keyboard.choose_subject(course))
                    break
            except ValueError:
                continue

        async def choose_subject():
            if len(subject_array_selected) == 0:
                if subject == data:
                    valid_subject["subject"] = subject
                    await call.answer("Предмет выбран")
                    await dp.bot.edit_message_text(chat_id=call.from_user.id,
                                                   message_id=call.message.message_id,
                                                   text=message_menu,
                                                   reply_markup=keyboard.choose_course())
                    subject_array_selected.append({"course": valid_subject["course"], "subject": valid_subject["subject"]})
                    print(subject_array_selected)
            else:
                for subject_selected in subject_array_selected:
                    if subject == data and data != subject_selected["subject"]:
                        valid_subject["subject"] = subject
                        await call.answer("Предмет выбран")
                        await dp.bot.edit_message_text(chat_id=call.from_user.id,
                                                       message_id=call.message.message_id,
                                                       text=message_menu,
                                                       reply_markup=keyboard.choose_course())
                        subject_array_selected.append({"course": valid_subject["course"], "subject": valid_subject["subject"]})
                        print(subject_array_selected)
                        break
                    if subject == data and data == subject_selected["subject"]:
                        await call.answer("Предмет уже выбран")
                        break

        array_subject = ["Математика", "Информатика",
                         "Основы веб технологий",
                         "Операционные системы",
                         "ООП", "Операционные системы",
                         "Английский язык", "БЖД"]

        for subject in array_subject:
            await choose_subject()

        if data == "confirm":
            check = True
            if len(subject_array_selected) != 0:
                for item in subject_array_selected:
                    for i in range(len(data_base.ItemsTeacher.query.all())):
                        try:
                            if item["subject"] == data_base.ItemsTeacher.query.filter(
                                    data_base.ItemsTeacher.teacher == call.message.chat.id).all()[i].subject:
                                await call.answer(f'Запись "{item["subject"]}" уже существует')
                                subject_array_selected.clear()
                                check = False
                        except:
                            continue
            if check:
                if len(subject_array_selected) != 0:
                    for item in subject_array_selected:
                        try:
                            db.register(chat_id=call.from_user.id,
                                        status="teacher",
                                        course=item["course"],
                                        subject=item["subject"])
                        except:
                            continue
                    db.stage(chat_id=call.from_user.id, stage="main_menu")
                    await dp.bot.edit_message_text(chat_id=call.from_user.id,
                                                   message_id=call.message.message_id,
                                                   text="Настройки сохранены")
                    subject_array_selected.clear()

                else:
                    await call.answer("Вы не заполнили форму")

        if data == "student":
            await dp.bot.edit_message_text(chat_id=call.from_user.id,
                                           message_id=call.message.message_id,
                                           text=message_status)


if __name__ == '__main__':
    executor.start_polling(dp)
