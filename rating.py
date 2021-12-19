import data_base
from data_base import *
''' Вывод рейтинга пользователей '''


def rating():
    global text
    users = list(set(Message.query.with_entities(Message.chat_id_respondent)))
    for i in range(len(users)):
        try:
            like_user = Message.query.filter_by(chat_id_respondent=users[i][0]).with_entities(Message.like)
            dislike_user = Message.query.filter_by(chat_id_respondent=users[i][0]).with_entities(Message.dislike)
            sum_like = 0
            for l in like_user:
                print(l[0])
                sum_like += l[0]
            sum_dislike = 0
            for d in dislike_user:
                sum_dislike += d[0]
            percent = (sum_like + sum_dislike)/100
            positive_rating = sum_like / percent
            print(positive_rating)
            data_base.positive_rating(chat_id=users[i][0], pr=positive_rating)
            data_base.like_dislike_user(chat_id=users[i][0], likes=sum_like, dislikes=sum_dislike)
        except:
            continue


def show_rating():
    rating()
    array = []
    text = "\n"
    user = Users.query.order_by(Users.positive_rating.desc()).all()
    for u in user:
        if len(Message.query.filter_by(chat_id_respondent=u.chat_id).with_entities(Message.like).all()) == 0:
            u.like = 0
            u.dislike = 0
            u.positive_rating = 0
        if u.positive_rating >= 50 and u.counter_answer > 5:
            text += f' {u.nikname}'
            text += f' 👍 {u.like} '
            text += f' 👎 {u.dislike} '
            text += f" %{'%.2f' % u.positive_rating}"
            text += f" 📋{u.counter_answer} \n"

    array.append(text)
    return '\n'.join(map(str, array))


