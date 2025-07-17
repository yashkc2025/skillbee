from flask import Blueprint,request
from .models import Admin, Session, Parent, Child, Skill, Lesson, LessonHistory, Activity, ActivityHistory, Quiz, QuizHistory, Badge, BadgeHistory
from .db import db
from .demoData import createDummyData
from .controllers import create_quiz,create_activity, create_badge, create_lesson, parent_regisc,child_regisc,admin_loginc,parent_loginc, child_loginc,get_auser,get_child_dashboard_stats,get_user_skill_progress,get_user_badges,get_lesson_quizzes,get_quiz_history,get_curriculums_for_child,get_children,get_parents,get_lessons,get_quizzes,get_activities,get_badges,create_child


api = Blueprint('api', __name__)

@api.route('/dummyData', methods=['GET'])
def dummyData():
    createDummyData()
    return "Dummy data has been created!"

@api.route('/auth/parent_register',methods=['POST'])
def parent_register():
    # Route for Parent Registration
    return parent_regisc(request)

@api.route('/auth/children_register',methods=['POST'])
def child_register():
    # Route for Children Registration
    return child_regisc(request)

@api.route('/auth/admin_login',methods=['POST'])
def admin_login():
    # Route for admin login
    return admin_loginc()

@api.route('/auth/parent_login',methods=['POST'])
def parent_login():
    """
    Route for parent login
    """
    
    return parent_loginc(request)

@api.route('/auth/children_login', methods=['POST'])
def child_login():
    """ 
    Route for child login
    """
    return child_loginc(request)

@api.route('/auth/get_user',methods=['GET'])
def get_user():
    return get_auser()

# @api.route('/get_user_details',methods=['GET'])
# def get_user_details():
#     return fetch_user_details(request) 

@api.route('/child_dashboard_stats', methods=['GET'])
def child_dashboard_stats():
    return get_child_dashboard_stats(request)

@api.route('/skill_categories', methods=['GET'])
def get_skill_categories():
    return get_user_skill_progress(request)

@api.route('/user_badges', methods=['GET'])
def user_badges():
    return get_user_badges()

@api.route("/api/child/<int:child_id>/curriculum/<int:curriculum_id>/lesson/<int:lesson_id>/quizzes", methods=["GET"])
def get_quizes(child_id, curriculum_id, lesson_id):
    return get_lesson_quizzes(child_id, curriculum_id, lesson_id)

@api.route("/api/child/<int:child_id>/quiz/<int:quiz_id>/history", methods=["GET"])
def get_history(child_id, quiz_id):
    return get_quiz_history(child_id, quiz_id)

@api.route('/api/child/<int:child_id>/curriculums', methods=['GET'])
def get_curr(child_id):
    return get_curriculums_for_child(child_id)

@api.route('/children', methods=['GET'])
def get_child():
    return get_children()

@api.route('/parents', methods=['GET'])
def get_parent():
    return get_parents()

@api.route('/lessons', methods=['GET'])
def get_lesson():
    return get_lessons()

@api.route('/quizzes', methods=['GET'])
def get_quiz():
    return get_quizzes()

@api.route('/activities', methods=['GET'])
def get_activity():
    return get_activities()

@api.route('/badges', methods=['GET'])
def get_badge():
    return get_badges()

@api.route('/parent/children', methods=['POST'])
def parent_children():
    return create_child(request)

@api.route('/admin/badge', methods=['POST'])
def admin_badge():
    return create_badge()

@api.route('/admin/activity', methods=['POST'])
def admin_activity():
    return create_activity()

@api.route('/admin/lesson', methods=['POST'])
def admin_lesson():
    return create_lesson()

@api.route('/admin/quiz', methods=['POST'])
def admin_quiz():
    return create_quiz()
