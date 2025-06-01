from . import db
from sqlalchemy.dialects.sqlite import JSON
from datetime import datetime

class Admin(db.Model):
    admin_id = db.Column(db.BigInteger, primary_key=True)
    email_id = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)


class Session(db.Model):
    session_id = db.Column(db.Text, primary_key=True)
    session_information = db.Column(JSON)


class Parent(db.Model):
    parent_id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    email_id = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    profile_image = db.Column(db.Text)
    is_blocked = db.Column(db.Boolean, default=False)

    children = db.relationship('Child', backref='parent', lazy=True)
    activities = db.relationship('Activity', backref='parent', lazy=True)


class Child(db.Model):
    child_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    school = db.Column(db.Text)
    email_id = db.Column(db.Text)
    points = db.Column(db.Integer, default=0)
    streak = db.Column(db.Integer, default=0)
    last_login = db.Column(db.DateTime)
    profile_image = db.Column(db.Text)
    is_blocked = db.Column(db.Boolean, default=False)

    parent_id = db.Column(db.BigInteger, db.ForeignKey('parent.parent_id'))  # FK not primary

    quiz_histories = db.relationship('QuizHistory', backref='child', lazy=True)
    lesson_histories = db.relationship('LessonHistory', backref='child', lazy=True)
    activities = db.relationship('Activity', backref='child', lazy=True)
    badge_histories = db.relationship('BadgeHistory', backref='child', lazy=True)


class Skill(db.Model):
    skill_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    min_age = db.Column(db.Integer)
    max_age = db.Column(db.Integer)

    lessons = db.relationship('Lesson', backref='skill', lazy=True)


class Lesson(db.Model):
    lesson_id = db.Column(db.Integer, primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.skill_id'))
    title = db.Column(db.Text, nullable=False)
    content = db.Column(JSON)
    position = db.Column(db.Integer)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.quiz_id'), nullable=True)

    activities = db.relationship('Activity', backref='lesson', lazy=True)
    lesson_histories = db.relationship('LessonHistory', backref='lesson', lazy=True)


class LessonHistory(db.Model):
    lesson_history_id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('child.child_id'))
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.lesson_id'))


class Activity(db.Model):
    activity_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)

    child_id = db.Column(db.Integer, db.ForeignKey('child.child_id'))
    parent_id = db.Column(db.BigInteger, db.ForeignKey('parent.parent_id'))
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.lesson_id'))

    activity_histories = db.relationship('ActivityHistory', backref='activity', lazy=True)


class ActivityHistory(db.Model):
    activity_history_id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.activity_id'))
    answer = db.Column(db.Text)
    feedback = db.Column(db.Text)


class Quiz(db.Model):
    quiz_id = db.Column(db.Integer, primary_key=True)
    quiz_name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    questions = db.Column(JSON)
    answers = db.Column(JSON)
    time_duration = db.Column(db.DateTime)
    is_visible = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    badge_id = db.Column(db.BigInteger, db.ForeignKey('badge.badge_id'), nullable=True)

    quiz_histories = db.relationship('QuizHistory', backref='quiz', lazy=True)
    lessons = db.relationship('Lesson', backref='quiz', lazy=True)


class QuizHistory(db.Model):
    quiz_history_id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.quiz_id'))
    child_id = db.Column(db.Integer, db.ForeignKey('child.child_id'))
    score = db.Column(db.Integer)
    responses = db.Column(JSON)
    reward_history_id = db.Column(db.Integer, db.ForeignKey('badge_history.reward_history_id'), nullable=True)


class Badge(db.Model):
    badge_id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)

    badge_histories = db.relationship('BadgeHistory', backref='badge', lazy=True)
    quizzes = db.relationship('Quiz', backref='badge', lazy=True)


class BadgeHistory(db.Model):
    reward_history_id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('child.child_id'))
    badge_id = db.Column(db.BigInteger, db.ForeignKey('badge.badge_id'))
