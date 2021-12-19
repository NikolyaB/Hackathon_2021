from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher

import data_base
import keyboard

TOKEN = '5059252399:AAFRQIZffaX11dO1NQ9D6uAwAJ-TBxnGa7U'
TelegramBot = Bot(token=TOKEN)
dp = Dispatcher(TelegramBot)
db = data_base


''' Запуск бота '''
@dp.message_handler(commands=['start', 'начать'])
async def start(msg: types.Message):
    array = []
    for i in range(len(db.Users.query.all())):
        try:
            array.append(db.Users.query.all()[i].chat_id)
        except:
            continue
    if msg.chat.id in array:
        check = True
    else:
        check = False
    if check is False:
        await msg.answer(text="Привет! Придумай себе никнейм")
        data_base.reg_stage(chat_id=msg.chat.id, stage="start")
    else:
        await msg.answer(text="Вы уже зарегистрированы", reply_markup=keyboard.main_menu())
        data_base.stage(chat_id=msg.chat.id, stage="menu")


@dp.message_handler(content_types=['text'])
async def send_answer(msg: types.Message):
    chat_id = msg.from_user.id
    stage = data_base.Stage.query.filter_by(chat_id=chat_id).with_entities(data_base.Stage.stage)[0][0]
    '''Регистрация пользователя'''
    if stage == "start":
        data_base.register_user(chat_id=chat_id, nikname=msg.text, status="user")
        data_base.stage(chat_id=chat_id, stage="menu")
        await msg.bot.send_message(chat_id=chat_id,
                                   text=f"Приятно познакомится, {msg.text}",
                                   reply_markup=keyboard.main_menu())
    print(stage)

    ''' Переводит пользователя в исходное состояние '''
    if msg.text.lower() == "меню":
        await msg.answer(text="Исходное состояние", reply_markup=keyboard.main_menu())
        data_base.stage(chat_id=chat_id, stage="menu")

    ''' главное меню пользователя '''
    if stage == "menu":
        if msg.text == "🤔Задать вопрос":
            await msg.answer(text="Категории", reply_markup=keyboard.all_questions_answer(action="questions"))
        if msg.text == "💡Ответить на вопросы":
            await msg.answer(text="Категории", reply_markup=keyboard.all_questions_answer(action="answers"))
        if msg.text == "Мои вопросы📰":
            await msg.answer(text="Вопросы", reply_markup=keyboard.my_questions())
        if msg.text == "Мои ответы🧾":
            await msg.answer(text="Ваши ответы", reply_markup=keyboard.user_answer(chat_id_respondent=chat_id,
                                                                                   status="send", action="QuestionAnswer"))
        if msg.text == "👥Форум":
            await msg.answer(text="Форум", reply_markup=keyboard.all_questions_answer(action="forum"))
        if msg.text == "Рейтинг🏆":
            import rating
            await msg.answer(text=f"➖Рейтинг Лучших➖\n{rating.show_rating()}")

    elif stage == "questions_title":
        global title
        title = msg.text
        if msg.text.lower() != "меню":
            await msg.answer(text="Введите ваш вопрос")
            data_base.message_add(chat_id_applicant=chat_id, tittle=title)
            data_base.stage(chat_id, "questions_message")
        else:
            data_base.stage(chat_id, "menu")
            data_base.message_add(chat_id_applicant=chat_id, tittle=title)
            data_base.delete_message(id=id, chat_id_applicant=chat_id)

    elif stage == "questions_message":
        if msg.text.lower() != "меню":
            await msg.answer(text="Вопрос отправлен")
            data_base.stage(chat_id, "menu")
            data_base.message_add(chat_id_applicant=chat_id, message_question=msg.text, status="wait")
        else:
            data_base.delete_message(id=id, chat_id_applicant=chat_id)

    elif stage == "answer":
        if msg.text.lower() != "меню":
            await msg.answer(text="Ответ отправлен")
            data_base.message_add(chat_id_respondent=chat_id, message_answ=msg.text, status="send")
            data_base.counter_answer(chat_id=chat_id)
            data_base.stage(chat_id, "menu")
        else:
            data_base.delete_message(id=id, chat_id_applicant=chat_id)

    else:
        data_base.stage(chat_id, stage="menu")


@dp.callback_query_handler(text_contains=['cancel'])
async def process_callback_kb1btn1(call: types.CallbackQuery):
    if call.data and call.data.startswith("cancel"):
        cancel = call.data
        chat_id = call.from_user.id
        data_base.stage(chat_id=chat_id, stage="menu")
        if cancel == "cancel":
            await call.bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)


@dp.callback_query_handler(text_contains=['category_'])
async def process_callback_kb1btn1(call: types.CallbackQuery):
    if call.data and call.data.startswith("category_"):
        chat_id = call.from_user.id
        print(call.data.split("_"))
        category = call.data.split("_")[1]
        action = call.data.split("_")[2]
        array = ["разработка", "тестирование", "аналитик",
                 "админ", "иб", "дизайн"]
        print(category)
        for item in array:
            if item == category:
                if action == "questions":
                    await call.bot.send_message(chat_id=chat_id, text="Введите заголовок вопроса",
                                                reply_markup=keyboard.cancel())
                    data_base.stage(chat_id=chat_id, stage="questions_title")
                    data_base.generation_message(chat_id_applicant=chat_id, category=category,
                                                 title="none", message="none", status="none")
        for item in array:
            if item == category:
                if action == "answers":
                    print(item)
                    await call.bot.send_message(chat_id=chat_id, text="Выберете вопрос",
                                                reply_markup=keyboard.user_all_questions(category=category, status="wait",
                                                                                         point="allquestions"))
        for item in array:
            if item == category:
                if action == "forum":
                    print(action)
                    await call.bot.send_message(chat_id=chat_id, text="Выберете вопрос",
                                                reply_markup=keyboard.user_all_questions(item, "send",
                                                                                         point="forum"))


@dp.callback_query_handler(text_contains=['allquestions_'])
async def process_callback_kb1btn1(call: types.CallbackQuery):
    if call.data and call.data.startswith("allquestions_"):
        chat_id = call.from_user.id
        category = call.data.split("_")[1]
        title = call.data.split("_")[2]
        id = call.data.split("_")[3]
        message_title = data_base.Message.query.filter_by(category=category).with_entities(
            data_base.Message.title).all()
        for t in message_title:
            if t[0] == title:
                message = data_base.Message.query.filter_by(id=id).with_entities(
                    data_base.Message.message_question).all()[0][0]
                print("message", message)
                await call.bot.edit_message_text(chat_id=chat_id,
                                                 text=f"Вопрос пользователя: \n{message}",
                                                 message_id=call.message.message_id,
                                                 reply_markup=keyboard.answer_on_message(title=title, id=id))


@dp.callback_query_handler(text_contains=['questions_'])
async def process_callback_kb1btn1(call: types.CallbackQuery):
    global id, action
    if call.data and call.data.startswith("questions_"):
        chat_id = call.from_user.id
        print(call.data.split("_"))
        call_data = call.data.split("_")[1]
        title = call.data.split("_")[1]
        if len(call.data.split("_")) >= 3:
            id = call.data.split("_")[2]
            action = call.data.split("_")[3]

        if call_data == "no-check":
            await call.bot.edit_message_text(chat_id=chat_id,
                                             text="Ваши вопросы",
                                             message_id=call.message.message_id,
                                             reply_markup=keyboard.user_questions(chat_id_applicant=chat_id,
                                                                                  status="wait", action="Question"))

        mesage_status = data_base.Message.query.filter_by(chat_id_applicant=chat_id).with_entities(
            data_base.Message.status).all()
        print(mesage_status)
        if call_data == "check":
            await call.bot.edit_message_text(chat_id=chat_id,
                                             text="Ваши вопросы",
                                             message_id=call.message.message_id,
                                             reply_markup=keyboard.user_questions(chat_id_applicant=chat_id,
                                                                                  status="send", action="QuestionAnswer"))
        print(call_data)
        if action == "Question":
            message_title = data_base.Message.query.filter_by(chat_id_applicant=chat_id).with_entities(
                data_base.Message.title).all()
            for t in message_title:
                if t[0] == title:
                    message = data_base.Message.query.filter_by(id=id).with_entities(
                        data_base.Message.message_question).all()[0][0]
                    await call.bot.edit_message_text(chat_id=chat_id,
                                                    text=f"Ваш вопрос: \n{message}",
                                                    message_id=call.message.message_id,
                                                    reply_markup=keyboard.delete_message(id=id, point="questions_back"))
        if action == "QuestionAnswer":
            message_title = data_base.Message.query.filter_by(chat_id_applicant=chat_id).with_entities(
                data_base.Message.title).all()
            for t in message_title:
                if t[0] == title:
                    message_question = data_base.Message.query.filter_by(id=id).with_entities(
                        data_base.Message.message_question).all()[0][0]
                    message_answer = data_base.Message.query.filter_by(id=id).with_entities(
                        data_base.Message.message_answer).all()[0][0]
                    await call.bot.edit_message_text(chat_id=chat_id,
                                                     text=f"Ваш вопрос: \n{message_question}\n"
                                                          f"Ответ: \n{message_answer}\n",
                                                     message_id=call.message.message_id,
                                                     reply_markup=keyboard.delete_message(id=id, point="questions_back"))

        if call_data == "back":
            await call.bot.edit_message_text(chat_id=chat_id,
                                             text="Ваши вопросы",
                                             message_id=call.message.message_id,
                                             reply_markup=keyboard.user_questions(chat_id_applicant=chat_id,
                                                                                  status="wait",
                                                                                  action="Question"))


@dp.callback_query_handler(text_contains=['answer_'])
async def process_callback_kb1btn1(call: types.CallbackQuery):
    global id, action
    if call.data and call.data.startswith("answer_"):
        chat_id = call.from_user.id
        print(call.data.split("_"))
        call_data = call.data.split("_")[1]
        title = call.data.split("_")[1]
        if len(call.data.split("_")) >= 3:
            id = call.data.split("_")[2]
            action = call.data.split("_")[3]


        mesage_status = data_base.Message.query.filter_by(chat_id_applicant=chat_id).with_entities(
            data_base.Message.status).all()
        print(mesage_status)
        print(call_data)
        if action == "QuestionAnswer":
            message_title = data_base.Message.query.filter_by(chat_id_applicant=chat_id).with_entities(
                data_base.Message.title).all()
            for t in message_title:
                if t[0] == title:
                    message_question = data_base.Message.query.filter_by(id=id).with_entities(
                        data_base.Message.message_question).all()[0][0]
                    message_answer = data_base.Message.query.filter_by(id=id).with_entities(
                        data_base.Message.message_answer).all()[0][0]
                    await call.bot.edit_message_text(chat_id=chat_id,
                                                     text=f"Вопрос: \n{message_question}\n\n"
                                                          f"Ваш ответ: \n{message_answer}\n",
                                                     message_id=call.message.message_id,
                                                     reply_markup=keyboard.message_menu("answer_back"))
        if call_data == "back":
            await call.bot.edit_message_text(chat_id=chat_id,
                                             text="Ваши ответы",
                                             message_id=call.message.message_id,
                                             reply_markup=keyboard.user_answer(chat_id_respondent=chat_id,
                                             status="send",
                                             action="QuestionAnswer"))


@dp.callback_query_handler(text_contains=['message_', ])
async def process_callback_kb1btn1(call: types.CallbackQuery):
    global title
    if call.data and call.data.startswith("message_"):
        chat_id = call.from_user.id
        print(call.data.split("_"))
        action = call.data.split("_")[1]
        if action != "like" and action != "dislike":
            title = call.data.split("_")[2]
        if len(call.data.split("_")) == 3:
            id = call.data.split("_")[2]
        else:
            id = call.data.split("_")[3]
        if action == "delete":
            data_base.delete_message(id=id, chat_id_applicant=chat_id)
            await call.bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
            await call.bot.send_message(chat_id=chat_id, text="Вопрос удален")

        if action == "answ":
            await call.bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.message_id,
                                             reply_markup=keyboard.cancel())
            data_base.message_add(chat_id_respondent=chat_id, id=id)
            db.stage(chat_id=chat_id, stage="answer")

        if action == "complaint":
            print(title)
            print(id)
            data_base.message_change_status(title=title, id=id, stat="block")
            await call.bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                                             text="Жалоба отправлена")
        print(action)
        async def like_dislike():
            message_question = data_base.Message.query.filter_by(id=id).with_entities(
                data_base.Message.message_question).all()[0][0]
            message_answer = data_base.Message.query.filter_by(id=id).with_entities(
                data_base.Message.message_answer).all()[0][0]
            message_like = data_base.Message.query.filter_by(id=id).with_entities(
                data_base.Message.like).all()[0][0]
            message_dislike = data_base.Message.query.filter_by(id=id).with_entities(
                data_base.Message.dislike).all()[0][0]
            await call.bot.edit_message_text(chat_id=chat_id,
                                             message_id=call.message.message_id,
                                             text=f"Вопрос: \n{message_question}\n\n"
                                                  f"Ответ: \n{message_answer}\n",
                                             reply_markup=keyboard.message_menu(like=message_like,
                                                                                dislike=message_dislike,
                                                                                message_id=id))
        if action == "like":
            await call.answer(text="LIKE")
            data_base.like_dislike_message(id, like="like")
            await like_dislike()
        if action == "dislike":
            await call.answer(text="DISLIKE")
            data_base.like_dislike_message(id, dislike="dislike")
            await like_dislike()


@dp.callback_query_handler(text_contains=['forum_'])
async def process_callback_kb1btn1(call: types.CallbackQuery):
    global id, action, message_id, category_back, title
    if call.data and call.data.startswith("forum_"):
        chat_id = call.from_user.id
        print(call.data.split("_"))
        category = call.data.split("_")[1]
        if len(call.data.split("_")) == 2:
            category_back = call.data.split("_")[1]
        if len(call.data.split("_")) >= 4:
            title = call.data.split("_")[2]
            message_id = call.data.split("_")[3]
        message_title = data_base.Message.query.filter_by(id=message_id, category=category).with_entities(
            data_base.Message.title).all()
        for t in message_title:
            if t[0] == title:
                message_question = data_base.Message.query.filter_by(id=message_id).with_entities(
                    data_base.Message.message_question).all()[0][0]
                message_answer = data_base.Message.query.filter_by(id=message_id).with_entities(
                    data_base.Message.message_answer).all()[0][0]
                message_like = data_base.Message.query.filter_by(id=message_id).with_entities(
                    data_base.Message.like).all()[0][0]
                message_dislike = data_base.Message.query.filter_by(id=message_id).with_entities(
                    data_base.Message.dislike).all()[0][0]
                await call.bot.edit_message_text(chat_id=chat_id,
                                                 text=f"Вопрос: \n{message_question}\n\n"
                                                      f"Ответ: \n{message_answer}\n",
                                                 message_id=call.message.message_id,
                                                 reply_markup=keyboard.message_menu(like=message_like,
                                                                                    dislike=message_dislike,
                                                                                    title=title,
                                                                                    message_id=message_id))
if __name__ == '__main__':
    executor.start_polling(dp)
