from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

import data_base


def main_menu():
    fourm = InlineKeyboardButton(text="Фоурм")
    ask_a_question = InlineKeyboardButton(text="Задать вопрос")
    answer_the_questions = InlineKeyboardButton(text="Ответить на вопросы")
    my_questions = InlineKeyboardButton(text="Мои вопросы")
    my_answers = InlineKeyboardButton(text="Мои ответы")
    rating = InlineKeyboardButton(text="Рейтинг")
    main_menu = InlineKeyboardButton(text="Меню")
    menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(ask_a_question, my_questions,
                                                                      answer_the_questions,
                                                                      my_answers,
                                                                      fourm, rating, main_menu)
    return menu


def all_questions_answer(action=None):
    questions = InlineKeyboardMarkup(row_width=2)
    development = InlineKeyboardButton("Разработка", callback_data="category_разработка_"+action)
    testing = InlineKeyboardButton("Тестирование", callback_data="category_тестирование_"+action)
    analytics = InlineKeyboardButton("Аналитика", callback_data="category_аналитика_"+action)
    administration = InlineKeyboardButton("Администрирование", callback_data="category_администрирование_"+action)
    information_security = InlineKeyboardButton("Информационная \nбезопасноть", callback_data="category_иб_"+action)
    design = InlineKeyboardButton("Дизайн", callback_data="category_дизайн_"+action)
    formulation = InlineKeyboardButton("Описание категории", callback_data="category_"+action)
    questions.add(development, testing,analytics, administration, information_security, design)
    questions.row(formulation)
    return questions


def my_questions():
    questions = InlineKeyboardMarkup(row_width=2)
    under_consideration = InlineKeyboardButton("На расмотрении", callback_data="questions_no-check")
    resolved = InlineKeyboardButton("Решенные", callback_data="questions_check")
    questions.add(under_consideration, resolved)
    return questions


def user_questions(chat_id_applicant):
    questions = InlineKeyboardMarkup(row_width=2)
    message_title = data_base.Message.query.filter_by(chat_id_applicant=chat_id_applicant).with_entities(data_base.Message.title).all()
    for item in message_title:
        questions.add(InlineKeyboardButton(item[0], callback_data="questions_"+item[0]))
    return questions


def delete_message(title):
    message = InlineKeyboardMarkup(row_width=1)
    delete = InlineKeyboardButton("Удалить", callback_data="message_"+"delete_"+title)
    message.add(delete)
    return message


def my_answer():
    answer = InlineKeyboardMarkup(row_width=2)
    return answer
