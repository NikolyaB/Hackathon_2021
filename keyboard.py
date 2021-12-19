from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

import data_base


def main_menu():
    fourm = InlineKeyboardButton(text="Форум")
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
    analytics = InlineKeyboardButton("Аналитика", callback_data="category_аналитик_"+action)
    administration = InlineKeyboardButton("Администрирование", callback_data="category_админ_"+action)
    information_security = InlineKeyboardButton("ИБ", callback_data="category_иб_"+action)
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


def user_questions(chat_id_applicant=None, status=None, action=None):
    questions = InlineKeyboardMarkup(row_width=2)
    cancel = InlineKeyboardButton("Закрыть", callback_data="cancel")
    message = data_base.Message.query.filter_by(chat_id_applicant=chat_id_applicant, status=status).with_entities(data_base.Message.message_question).all()
    message_id = data_base.Message.query.filter_by(chat_id_applicant=chat_id_applicant, status=status).with_entities(data_base.Message.id).all()
    message_title = data_base.Message.query.filter_by(chat_id_applicant=chat_id_applicant, status=status).with_entities(data_base.Message.title).all()
    for i in range(len(message)):
        questions.add(InlineKeyboardButton(message_title[i][0], callback_data=f"questions_{message_title[i][0]}_{message_id[i][0]}_{action}"))
    questions.add(cancel)
    return questions


def user_answer(chat_id_respondent=None, status=None, action=None):
    questions = InlineKeyboardMarkup(row_width=2)
    message = data_base.Message.query.filter_by(chat_id_respondent=chat_id_respondent, status=status).with_entities(data_base.Message.message_question).all()
    message_id = data_base.Message.query.filter_by(chat_id_respondent=chat_id_respondent, status=status).with_entities(data_base.Message.id).all()
    message_title = data_base.Message.query.filter_by(chat_id_respondent=chat_id_respondent, status=status).with_entities(data_base.Message.title).all()
    for i in range(len(message)):
        questions.add(InlineKeyboardButton(message_title[i][0], callback_data=f"answer_{message_title[i][0]}_{message_id[i][0]}_{action}"))
    return questions


def user_all_questions(category, status, point):
    questions = InlineKeyboardMarkup(row_width=2)
    message = data_base.Message.query.filter_by(category=category, status=status).with_entities(
        data_base.Message.message_question).all()
    message_id = data_base.Message.query.filter_by(category=category, status=status).with_entities(
        data_base.Message.id).all()
    message_title = data_base.Message.query.filter_by(category=category, status=status).with_entities(
        data_base.Message.title).all()
    for i in range(len(message)):
        questions.add(InlineKeyboardButton(message_title[i][0],
                                           callback_data=f"{point}_{category}_{message_title[i][0]}_{message_id[i][0]}"))
    return questions


def delete_message(id, point=None):
    message = InlineKeyboardMarkup(row_width=1)
    if point is not None:
        back = InlineKeyboardButton("Назад", callback_data=point)
        message.add(back)
    delete = InlineKeyboardButton("Удалить", callback_data="message_delete_"+id)
    message.add(delete)
    return message


def answer_on_message(title, id):
    msg = InlineKeyboardMarkup(row_width=3)
    answer = InlineKeyboardButton("Ответить", callback_data=f"message_answ_{title}_{id}")
    complaint = InlineKeyboardButton("Жалоба", callback_data=f"message_complaint_{title}_{id}")
    msg.row(answer, complaint)
    return msg


def message_menu(point, message_id=None, like=None, dislike=None, category=None):
    menu = InlineKeyboardMarkup(row_width=1)
    if category is not None:
        back = InlineKeyboardButton("Назад", callback_data=f"{point}_{category}")
    else:
        back = InlineKeyboardButton("Назад", callback_data=point)
    if like is not None or dislike:
        like = InlineKeyboardButton(f"👍 {like}", callback_data=f"message_like_{message_id}")
        dislike = InlineKeyboardButton(f"👎 {dislike}", callback_data=f"message_dislike_{message_id}")
        menu.row(like, dislike)
    menu.add(back)
    return menu