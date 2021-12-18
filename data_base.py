from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/Bot.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, unique=True)
    like = db.Column(db.Integer, default=0)
    dislike = db.Column(db.Integer, default=0)
    counter_answer = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<users {self.id}>"


class Stage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, unique=True)
    stage = db.Column(db.String(50))
    counter = db.Column(db.Integer, default=0)


class MentorSubject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mentor_chat_id = db.Column(db.Integer)
    subject = db.Column(db.String(100))
    course = db.Column(db.Integer)


class MenteeSubject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mentee_chat_id = db.Column(db.Integer)
    speciality = db.Column(db.String(100))


def stage(chat_id, stage, counter=None):
    try:
        if counter is not None:
            stg = Stage(chat_id=chat_id, stage=stage, counter=counter)
        else:
            stg = Stage(chat_id=chat_id, stage=stage)
        db.session.add(stg)
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


# def register(chat_id, status=None, subject=None, course=None):
#     try:
#         if status is not None:
#             if len(Users.query.filter_by(chat_id=chat_id).all()) == 0:
#                 user = Users(chat_id=chat_id, status=status)
#                 db.session.add(user)
#             if status == "teacher":
#                 itemsteacher = ItemsTeacher(subject=subject, course=course, teacher=chat_id)
#                 db.session.add(itemsteacher)
#         db.session.flush()
#         db.session.commit()
#     except:
#         db.session.rollback()
#         print("Ошибка добавления в БД")
#         return "Ошибка добавления в БД"


# def delete_teach_group(chat_id):
#     try:
#         if Users.query.filter_by(chat_id=chat_id).all()[0].id is not None:
#             id = Users.query.filter_by(chat_id=chat_id).all()[0].id
#             Users.query.filter_by(id=id).delete()
#             db.session.commit()
#     except:
#         db.session.rollback()
#         print("Ошибка удаления из БД")
#
#
# def subscribe(chat_id, time, group=None, teacher=None):
#     try:
#         if group is not None:
#             notification = Notification_group(chat_id=chat_id, group=group, time=time)
#             db.session.add(notification)
#         if teacher is not None:
#             notification = Notification_teacher(chat_id=chat_id, teacher=teacher, time=time)
#             db.session.add(notification)
#         db.session.flush()
#         db.session.commit()
#     except:
#         db.session.rollback()
#         print("Ошибка добавления в БД")


# def unsubscribe(chat_id, group=None, teacher=None):
#     try:
#         if group is not None:
#             notification = Notification_group.query.filter_by(chat_id=chat_id).all()
#             for i in range(len(Notification_group.query.filter_by(chat_id=chat_id).all())):
#                 if notification[i].group == group:
#                     Notification_group.query.filter_by(id=notification[i].id).delete()
#                     db.session.commit()
#         if teacher is not None:
#             notification = Notification_teacher.query.filter_by(chat_id=chat_id).all()
#             for i in range(len(Notification_teacher.query.filter_by(chat_id=chat_id).all())):
#                 if notification[i].teacher == teacher:
#                     Notification_teacher.query.filter_by(id=notification[i].id).delete()
#                     db.session.commit()
#     except:
#         db.session.rollback()
#         print("Ошибка удаления из БД")


if __name__ == '__main__':
    app.run(debug=True)
