from .database import db
from datetime import datetime as dt , timedelta
class User(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    username=db.Column(db.String(),unique=True,nullable=False)
    password=db.Column(db.String(),nullable=False)
    fullname=db.Column(db.String(),nullable=False,)
    qualification=db.Column(db.String(),nullable=False)
    dob=db.Column(db.String())
    type=db.Column(db.String(),default="general")
    scores = db.relationship('Score', backref='user', lazy=True)
class Subject(db.Model):
    id = db.Column(db.Integer(), primary_key=True,unique=True)
    name = db.Column(db.String(), nullable=False,unique=True)
    description = db.Column(db.Text())
    chapters = db.relationship('Chapter', backref='subject', lazy='dynamic')

class Chapter(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    description = db.Column(db.Text())
    subject_id = db.Column(db.Integer(), db.ForeignKey('subject.id'), nullable=False)
    quizzes = db.relationship('Quiz', backref='chapter', lazy='dynamic')

class Quiz(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    chapter_id = db.Column(db.Integer(), db.ForeignKey('chapter.id'), nullable=False)
    date_of_quiz = db.Column(db.DateTime())
    time_duration = db.Column(db.Integer(),nullable=False)  # in minutes
    questions = db.relationship('Question', backref='quiz', lazy='dynamic')
    scores = db.relationship('Score', backref='quiz', lazy=True, cascade="all, delete-orphan")



class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    option1 = db.Column(db.String(), nullable=False)
    option2 = db.Column(db.String(), nullable=False)
    option3 = db.Column(db.String(), nullable=False)
    option4 = db.Column(db.String(), nullable=False)
    correct_option = db.Column(db.Integer, nullable=False)
class Score(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer(), db.ForeignKey('quiz.id'), nullable=False)
    score = db.Column(db.Integer(), nullable=False)
    attempt_date = db.Column(db.DateTime())
