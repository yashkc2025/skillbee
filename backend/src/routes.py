from flask import Blueprint, jsonify, request
from .models import Admin, Session, Parent, Child, Skill, Lesson, LessonHistory, Activity, ActivityHistory, Quiz, QuizHistory, Badge, BadgeHistory
from . import db

api = Blueprint('api', __name__)

@api.route('/dummy', methods=['GET'])
def dummy():
    return "Hello, World!"