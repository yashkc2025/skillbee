from .db import db
from sqlalchemy import CheckConstraint, Index, UniqueConstraint
from sqlalchemy.dialects.sqlite import JSON
from datetime import datetime

class Admin(db.Model):
    admin_id = db.Column(db.Integer, primary_key=True)
    email_id = db.Column(db.Text, nullable=False, index=True)
    password = db.Column(db.Text, nullable=False)
    

class Session(db.Model):
    session_id = db.Column(db.Text, primary_key=True)
    session_information = db.Column(JSON, nullable=False)


class Parent(db.Model):
    parent_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    email_id = db.Column(db.Text, nullable=False, index=True)
    password = db.Column(db.Text, nullable=False)
    profile_image = db.Column(db.LargeBinary, nullable=True)
    is_blocked = db.Column(db.Boolean, default=False)

    children = db.relationship('Child', backref='parent', lazy=True)
    activities = db.relationship('Activity', backref='parent', lazy=True)


class Child(db.Model):
    child_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, nullable=False, index=True)
    password = db.Column(db.Text, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    school = db.Column(db.Text, nullable=True)
    email_id = db.Column(db.Text, nullable=True, index=True)
    points = db.Column(db.Integer, default=0)
    streak = db.Column(db.Integer, default=0)
    last_login = db.Column(db.DateTime, default=datetime(1970, 1, 1))
    enrollment_date = db.Column(db.DateTime, default=datetime.utcnow)
    profile_image = db.Column(db.LargeBinary, nullable=True)
    is_blocked = db.Column(db.Boolean, default=False)

    parent_id = db.Column(db.Integer, db.ForeignKey('parent.parent_id'), index=True)  

    quiz_histories = db.relationship('QuizHistory', backref='child', lazy=True)
    lesson_histories = db.relationship('LessonHistory', backref='child', lazy=True)
    activities = db.relationship('Activity', backref='child', lazy=True)
    badge_histories = db.relationship('BadgeHistory', backref='child', lazy=True)

    __table_args__ = (
    db.CheckConstraint("parent_id IS NOT NULL OR email_id IS NOT NULL", name="check_parent_or_email"),
    )


class Skill(db.Model):
    skill_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=True)
    min_age = db.Column(db.Integer, nullable=False)
    max_age = db.Column(db.Integer, nullable=False)

    lessons = db.relationship('Lesson', backref='skill', lazy=True)

    __table_args__ = (
        CheckConstraint('min_age >= 0', name='check_min_age_nonnegative'),
        CheckConstraint('max_age <= 120', name='check_max_age_maximum'),
        CheckConstraint('min_age <= max_age', name='check_min_le_max'),

    )


class Lesson(db.Model):
    lesson_id = db.Column(db.Integer, primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.skill_id'), nullable=False, index=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(JSON, nullable=False)
    position = db.Column(db.Integer, nullable=False)
    image = db.Column(db.LargeBinary, nullable=True)

    activities = db.relationship('Activity', backref='lesson', lazy=True)
    quizzes = db.relationship('Quiz', backref='lesson', lazy=True)
    lesson_histories = db.relationship('LessonHistory', backref='lesson', lazy=True)

    __table_args__ = (
        UniqueConstraint('skill_id', 'position', name='unique_lesson_position'),
    )



class LessonHistory(db.Model):
    lesson_history_id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('child.child_id'), nullable=False, index=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.lesson_id'), nullable=False, index=True)

    __table_args__ = (
        UniqueConstraint('child_id', 'lesson_id', name='unique_child_lesson'),
        db.Index('ix_lessonhistory_child_lesson', 'child_id', 'lesson_id'),
    )



class Activity(db.Model):
    activity_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    answer_format = db.Column(db.Text, nullable=True)
    instructions = db.Column(db.Text, nullable=True)
    difficulty = db.Column(db.Text, nullable=True)
    image = db.Column(db.LargeBinary, nullable=True)
    
    child_id = db.Column(db.Integer, db.ForeignKey('child.child_id'), index=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.parent_id'), index=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.lesson_id'))

    activity_histories = db.relationship('ActivityHistory', backref='activity', lazy=True)

    __table_args__ = (
        CheckConstraint(
            "answer_format IN ('text','image','pdf')",
            name='check_answer_format'
        ),
    )


class ActivityHistory(db.Model):
    activity_history_id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.activity_id'), nullable=False, index=True)
    answer = db.Column(db.LargeBinary)
    feedback = db.Column(db.Text)


class Quiz(db.Model):
    quiz_id = db.Column(db.Integer, primary_key=True)
    quiz_name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String,nullable=False)
    points = db.Column(db.Integer, nullable=False)
    image = db.Column(db.LargeBinary, nullable=True)
    questions = db.Column(JSON, nullable=False)
    answers = db.Column(JSON, nullable=False)
    time_duration = db.Column(db.Integer) # Duration of the test should be stored in seconds
    is_visible = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.lesson_id'), nullable=False, index=True)
    position = db.Column(db.Integer, nullable=False)
    badge_id = db.Column(db.Integer, db.ForeignKey('badge.badge_id'), nullable=True)

    quiz_histories = db.relationship('QuizHistory', backref='quiz', lazy=True)

    __table_args__ = (
        UniqueConstraint('lesson_id', 'position', name='unique_quiz_position'),
    )

    


class QuizHistory(db.Model):
    quiz_history_id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.quiz_id'), nullable=False)
    child_id = db.Column(db.Integer, db.ForeignKey('child.child_id'), nullable=False, index=True)
    score = db.Column(db.Integer, nullable=False)
    responses = db.Column(JSON, nullable=False)
    badge_history_id = db.Column(db.Integer, db.ForeignKey('badge_history.reward_history_id'), nullable=True)

    __table_args__ = (
        db.Index('ix_quizhistory_quiz_child', 'quiz_id', 'child_id'),
    )


class Badge(db.Model):
    badge_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.LargeBinary, nullable=True)
    badge_histories = db.relationship('BadgeHistory', backref='badge', lazy=True)
    quizzes = db.relationship('Quiz', backref='badge', lazy=True)


class BadgeHistory(db.Model):
    reward_history_id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('child.child_id'), index=True)
    badge_id = db.Column(db.Integer, db.ForeignKey('badge.badge_id'))
    awarded_on = db.Column(db.DateTime,default=datetime.utcnow )
    __table_args__ = (
        UniqueConstraint('child_id', 'badge_id', name='unique_child_badge'),
        db.Index('ix_badgehistory_child_badge', 'child_id', 'badge_id'),
    )
