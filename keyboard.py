from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

import data_base


def main_menu():
    fourm = InlineKeyboardButton(text="Фоурм")
    ask_a_question = InlineKeyboardButton(text="Задать вопрос")
    answer_the_questions = InlineKeyboardButton(text="Ответить на вопросы")
    my_questions = InlineKeyboardButton(text="Мои вопросы")
    my_answers = InlineKeyboardButton(text="Мои ответы")
    rating = InlineKeyboardButton(text="Рейтинг")
    menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(ask_a_question, my_questions,
                                                                      answer_the_questions,
                                                                      my_answers,
                                                                      fourm, rating)
    return menu


def all_questions_answer(data=None):
    questions = InlineKeyboardMarkup(row_width=2)
    development = InlineKeyboardButton("Разработка", callback_data="category_"+"разработка_"+data)
    testing = InlineKeyboardButton("Тестирование", callback_data="category_"+data)
    analytics = InlineKeyboardButton("Аналитика", callback_data="category_"+data)
    administration = InlineKeyboardButton("Администрирование", callback_data="category_"+data)
    information_security = InlineKeyboardButton("Информационная безопасноть", callback_data="category_"+data)
    design = InlineKeyboardButton("Дизайн", callback_data="category_"+data)
    formulation = InlineKeyboardButton("Описание категории", callback_data="category_"+data)
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
