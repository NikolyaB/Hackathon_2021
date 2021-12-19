from data_base import *
''' Вывод рейтинга пользователей '''


def rating():
    global text
    array = []
    users = list(set(Message.query.with_entities(Message.chat_id_respondent).all()))
    for i in range(len(users)):
        try:
            print(users[i][0])
            like_user = Message.query.filter_by(chat_id_respondent=users[i][0]).with_entities(Message.like)
            dislike_user = Message.query.filter_by(chat_id_respondent=users[i][0]).with_entities(Message.dislike)
            user = Users.query.filter_by(chat_id=users[i][0]).with_entities(Users.nikname)[0][0]
            counter_answer = Users.query.filter_by(chat_id=users[i][0]).with_entities(Users.counter_answer)[0][0]
            if counter_answer > 5:
                sum_like = 0
                for l in like_user:
                    sum_like += l[0]
                sum_dislike = 0
                for d in dislike_user:
                    sum_dislike += d[0]
                percent = (sum_like + sum_dislike)/100
                positive_rating = sum_like / percent
                print(sum_like, sum_dislike, counter_answer, "%.2f" % positive_rating)
                text = f'{i} {user}'
                text += f" 👍{'%.2f' % positive_rating}"
                text += f" 📋{counter_answer}"
        except:
            continue
    array.append(text)
    return '\n'.join(map(str, array))
