from data_base import *


def rating():
    array = []
    user = Users.query.with_entities(Users.nikname).order_by(Users.like.desc()).all()
    like = Users.query.with_entities(Users.like).order_by(Users.like.desc()).all()
    counter_answer = Users.query.with_entities(Users.counter_answer).order_by(Users.like.desc()).all()
    for i in range(len(user[:5])):
        text = f' \n{i+1} {user[i][0]}'
        text += f" 👍{like[i][0]}"
        text += f" 📋{counter_answer[i][0]}"
        array.append(text)
    return '\n'.join(map(str, array))
