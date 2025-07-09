from flask import Blueprint,request
from .models import Admin, Session, Parent, Child, Skill, Lesson, LessonHistory, Activity, ActivityHistory, Quiz, QuizHistory, Badge, BadgeHistory
from .db import db
from .demoData import createDummyData
from .controllers import parent_regisc,child_regisc,admin_loginc,parent_loginc, child_loginc,get_auser,get_child_dashboard_stats,get_user_skill_progress


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
