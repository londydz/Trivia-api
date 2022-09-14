import os
from pathlib import Path
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from dotenv import load_dotenv

load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)
database_name = os.getenv["DB_NAME "]
path = os.path.dotenv(os.path.dotenv(".env"))
database_user = os.getenv["DB_USER"]
password = os.getenv["DB_PASSWORD "]

database_path = os.getenv["DB_PATH"]

#database_name = 'trivia'
# database_path = "postgresql://{}:{}@{}/{}".format(
#   "postgres", "pass", "localhost:5432", database_name
# )
db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


"""
Question

"""


class Question(db.Model):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    category = Column(String)
    difficulty = Column(Integer)

    def __init__(self, question, answer, category, difficulty):
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category,
            'difficulty': self.difficulty
        }


"""
Category

"""


class Category(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    type = Column(String)

    def __init__(self, type):
        self.type = type

    def format(self):
        return {
            'id': self.id,
            'type': self.type
        }


"""
Category

"""


class Leaderboard(db.Model):
    __tablename__ = 'leaderboard'

    id = Column(Integer, primary_key=True)
    player = Column(String)
    score = Column(Integer)

    def __init__(self, player, score):
        self.player = player
        self.score = score

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'player': self.player,
            'score': self.score,
        }
