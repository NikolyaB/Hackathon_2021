from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/Bot.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, unique=True)
    nikname = db.Column(db.String(25), unique=True)
    status = db.Column(db.String(25))
    like = db.Column(db.Integer, default=0)
    dislike = db.Column(db.Integer, default=0)
    counter_answer = db.Column(db.Integer, default=0)
    positive_rating = db.Column(db.Float, default=0)

    def __repr__(self):
        return f"<users {self.id}>"


class Stage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, unique=True)
    stage = db.Column(db.String(50))
    counter = db.Column(db.Integer, default=0)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id_applicant = db.Column(db.Integer)
    chat_id_respondent = db.Column(db.Integer)
    category = db.Column(db.String(50))
    title = db.Column(db.String(100))
    message_question = db.Column(db.String(500))
    message_answer = db.Column(db.String(500))
    like = db.Column(db.Integer, default=0)
    dislike = db.Column(db.Integer, default=0)
    status = db.Column(db.String(10))


def generation_message(chat_id_applicant, category, title, message, status):
    try:
        message = Message(chat_id_applicant=chat_id_applicant,
                          category=category, title=title,
                          message_question=message, status=status)
        db.session.add(message)
        db.session.flush()
        db.session.commit()
    except:
        db.session.rollback()
        print("Ошибка добавления в БД")


def message_add(chat_id_applicant=None, id=None, chat_id_respondent=None,  tittle=None, message_question=None, message_answ=None, status=None):
    try:
        if tittle is not None:
            Message.query.filter_by(chat_id_applicant=chat_id_applicant, title="none").all()[0].title = tittle
            db.session.flush()
            db.session.commit()
        if message_question is not None:
            Message.query.filter_by(chat_id_applicant=chat_id_applicant, message_question="none").all()[0].message_question = message_question
            db.session.flush()
            db.session.commit()
        if status is not None and chat_id_applicant is not None:
            Message.query.filter_by(chat_id_applicant=chat_id_applicant, status="none").all()[0].status = status
            db.session.flush()
            db.session.commit()
        if chat_id_respondent is not None and id is not None:
            Message.query.filter_by(id=id, status="wait").all()[0].chat_id_respondent = chat_id_respondent
        if message_answ is not None and chat_id_respondent is not None:
            Message.query.filter_by(chat_id_respondent=chat_id_respondent, status="wait").all()[0].message_answer = message_answ
            Message.query.filter_by(chat_id_respondent=chat_id_respondent, status="wait").all()[0].status = status
    except:
        db.session.rollback()
        print("Ошибка добавления в БД")


def message_change_status(title, id, stat):
    try:
        print(id)
        Message.query.filter_by(title=title, id=id).all()[0].status = stat
        db.session.flush()
        db.session.commit()
    except:
        db.session.rollback()
        print("Ошибка в изменении статуса")


def delete_message(id, chat_id_applicant):
    try:
        Message.query.filter_by(id=id, chat_id_applicant=chat_id_applicant).delete()
        db.session.flush()
        db.session.commit()
    except:
        db.session.rollback()
        print("Ошибка удаления из БД")


def reg_stage(chat_id, stage):
    try:
        stage = Stage(chat_id=chat_id, stage=stage)
        db.session.add(stage)
        db.session.flush()
        db.session.commit()
    except:
        db.session.rollback()
        print("Ошибка добавления в БД")


def stage(chat_id, stage):
    try:
        Stage.query.filter_by(chat_id=chat_id)[0].stage = stage
        db.session.flush()
        db.session.commit()
    except:
        db.session.rollback()
        print("Ошибка добавления в БД")


def delete_stage(chat_id):
    try:
        if Stage.query.filter_by(chat_id=chat_id).all()[0].id is not None:
            id = Stage.query.filter_by(chat_id=chat_id).all()[0].id
            Stage.query.filter_by(id=id).delete()
            db.session.commit()
    except:
        db.session.rollback()
        print("Ошибка удаления из БД")


def register_user(chat_id, nikname, status):
    try:
        user = Users(chat_id=chat_id, nikname=nikname, status=status)
        db.session.add(user)
        db.session.flush()
        db.session.commit()
    except:
        db.session.rollback()
        print("Ошибка добавления в БД")


def delete_user(chat_id):
    try:
        Users.query.filter_by(chat_id=chat_id).delete()
    except:
        db.session.rollback()
        print("Ошибка удаления в БД")


def rename_user(chat_id, nikname):
    try:
        Users.query.filter_by(chat_id=chat_id).all()[0].nikname = nikname
        db.session.flush()
        db.session.commit()
    except:
        db.session.rollback()
        print("Ошибка добавления в БД")


def change_status_user(chat_id, status):
    try:
        Users.query.filter_by(chat_id=chat_id).all()[0].status = status
        db.session.flush()
        db.session.commit()
    except:
        db.session.rollback()
        print("Ошибка добавления в БД")


def like_dislike_message(id, like=None, dislike=None):
    try:
        if like is not None:
            Message.query.filter_by(id=id).all()[0].like += 1
            db.session.flush()
            db.session.commit()
        if dislike is not None:
            Message.query.filter_by(id=id).all()[0].dislike += 1
            db.session.flush()
            db.session.commit()
    except:
        db.session.rollback()
        print("Ошибка добавления в БД")


def positive_rating(chat_id, pr):
    try:
        Users.query.filter_by(chat_id=chat_id).order_by(Users.positive_rating)[0].positive_rating = pr
        db.session.flush()
        db.session.commit()
    except:
        db.session.rollback()
        print("Ошибка добавления в БД")


def like_dislike_user(chat_id, likes=None, dislikes=None):
    try:
        if likes is not None:
            Users.query.filter_by(chat_id=chat_id).all()[0].like = likes
            db.session.flush()
            db.session.commit()
        if dislikes is not None:
            Users.query.filter_by(chat_id=chat_id).all()[0].dislike = dislikes
            db.session.flush()
            db.session.commit()
    except:
        db.session.rollback()
        print("Ошибка добавления в БД")

def counter_answer(chat_id):
    try:
        Users.query.filter_by(chat_id=chat_id).all()[0].counter_answer += 1
        db.session.flush()
        db.session.commit()
    except:
        db.session.rollback()
        print("Ошибка добавления в БД")


if __name__ == '__main__':
    app.run(debug=True)
