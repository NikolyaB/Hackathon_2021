from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


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
    development = InlineKeyboardButton("Разработка", callback_data=data)
    testing = InlineKeyboardButton("Тестирование", callback_data=data)
    analytics = InlineKeyboardButton("Аналитика", callback_data=data)
    administration = InlineKeyboardButton("Администрирование", callback_data=data)
    information_security = InlineKeyboardButton("Информационная безопасноть", callback_data=data)
    design = InlineKeyboardButton("Дизайн", callback_data="dev")
    questions.add(development, testing,analytics, administration, information_security, design)
    return questions


def my_questions():
    questions = InlineKeyboardMarkup(row_width=2)
    under_consideration = InlineKeyboardButton("На расмотрении", callback_data="w")
    resolved = InlineKeyboardButton("Решенные", callback_data="w")
    questions.add(under_consideration, resolved)
    return questions


def my_answer():
    answer = InlineKeyboardMarkup(row_width=2)
    return answer
