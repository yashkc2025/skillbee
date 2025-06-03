from flask import Blueprint,request
from .models import Admin, Session, Parent, Child, Skill, Lesson, LessonHistory, Activity, ActivityHistory, Quiz, QuizHistory, Badge, BadgeHistory
from .db import db
from .demoData import createDummyData
<<<<<<< HEAD
from .controllers import parent_regisc,child_regisc,admin_loginc
=======
from .controllers import parent_regisc,child_regisc,parent_loginc, child_loginc
>>>>>>> 6e0691b (feat: implemented login system)


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
<<<<<<< HEAD
    # Route for Children Registration
    return child_regisc(request)

@api.route('/auth/admin_login',methods=['POST'])
def admin_login():
    # Route for admin login
    return admin_loginc()
=======
    return child_regisc(request)

@api.route('/auth/parent_login',methods=['POST'])
def parent_login():
    return parent_loginc(request)

@api.route('/auth/children_login', methods=['POST'])
def child_login():
    return child_loginc(request)
>>>>>>> 6e0691b (feat: implemented login system)
