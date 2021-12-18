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


def stage(chat_id, stage, counter=None):
    try:
        if counter is not None:
            stg = Stage(chat_id=chat_id, stage=stage, counter=counter+1)
        else:
            stg = Stage(chat_id=chat_id, stage=stage)
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


def register(chat_id, status=None, subject=None, course=None):
    try:
        if status is not None:
            if len(Users.query.filter_by(chat_id=chat_id).all()) == 0:
                user = Users(chat_id=chat_id, status=status)
                db.session.add(user)
            if status == "teacher":
                itemsteacher = ItemsTeacher(subject=subject, course=course, teacher=chat_id)
                db.session.add(itemsteacher)
        db.session.flush()
        db.session.commit()
    except:
        db.session.rollback()
        print("Ошибка добавления в БД")
        return "Ошибка добавления в БД"





if __name__ == '__main__':
    app.run(debug=True)
