from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


def choose_status():
    status = InlineKeyboardMarkup(row_width=2)
    mentee = InlineKeyboardButton("Менти", callback_data="status_student")
    mentor = InlineKeyboardButton("Ментор", callback_data="status_teacher")
    status.add(mentee, mentor)
    return status


def choose_course():
    courses = InlineKeyboardMarkup(row_width=1)
    back = InlineKeyboardButton("Назад", callback_data="status_back")
    array = [1, 2, 3, 4]
    courses.add(back)
    for course in array:
        courses.add(InlineKeyboardButton(course, callback_data=f"status_{course}"))
    confirm = InlineKeyboardButton("Подтвердить", callback_data="status_confirm")
    courses.add(confirm)
    return courses


def choose_subject(course):
    subjects = InlineKeyboardMarkup(row_width=1)
    back = InlineKeyboardButton("Назад", callback_data=f"status_back-menu")
    if course == 1:
        array = ["Математика", "Информатика"]
    if course == 2:
        array = ["Основы веб технологий", "Операционные системы"]
    if course == 3:
        array = ["ООП", "Операционные системы"]
    if course == 4:
        array = ["Английский язык", "БЖД"]
    subjects.add(back)
    for subject in array:
        subjects.add(InlineKeyboardButton(subject, callback_data=f"status_{subject}"))
    return subjects


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
