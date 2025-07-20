from flask import Blueprint, request, jsonify
from .models import Admin, Session, Parent, Child, Skill, Lesson, LessonHistory, Activity, ActivityHistory, Quiz, QuizHistory, Badge, BadgeHistory
from .db import db
from .demoData import createDummyData
from functools import wraps
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta
from flask_apscheduler import APScheduler
from .controllers import (
    # Auth related functions
    parent_regisc,
    child_regisc,
    admin_loginc,
    parent_loginc,
    child_loginc,
    # Child related functions
    get_skill_lessons,
    get_lesson_details,
    mark_lesson_completed,
    get_lesson_activities,
    get_lesson_quizzes,
    get_activity_details,
    submit_activity,
    get_activity_history,
    get_activity_submission,
    get_quiz_history,
    get_quiz_questions,
    submit_quiz,
    get_child_profile,
    update_child_profile,
    change_child_password,
    child_profile_image
)

scheduler = APScheduler()

api = Blueprint('api', __name__)

def configure_scheduler(app):
    """Configure the APScheduler for session cleanup"""
    scheduler.init_app(app)
    
    def wrapped_cleanup():
        with app.app_context():
            cleanup_expired_sessions()
    
    # Run cleanup immediately when application starts
    wrapped_cleanup()
    
    # Add job to run every hour
    scheduler.add_job(
        id='cleanup_sessions',
        func=wrapped_cleanup,  
        trigger='interval',
        hours=1,  
        max_instances=1,  
        next_run_time=datetime.now() + timedelta(hours=1)  
    )
    
    # Start the scheduler
    scheduler.start()

def cleanup_expired_sessions():
    try:
        expiry_time = datetime.now() - timedelta(hours=3)
        expired_sessions = [
            session for session in Session.query.all()
            if datetime.fromisoformat(session.session_information['login_time']) < expiry_time
        ]
        
        for session in expired_sessions:
            db.session.delete(session)
        db.session.commit()
        
        print(f"Cleaned up {len(expired_sessions)} expired sessions")
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Database error: {str(e)}")
    except (KeyError, ValueError) as e:
        print(f"Data format error: {str(e)}")


def token_required(allowed_roles=None):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            if 'Authorization' in request.headers:
                token = request.headers['Authorization'].split(' ')[-1] 
                print(token)
            
            if not token:
                return jsonify({'error': 'Token is missing'}), 401

            try:
                session = Session.query.filter_by(session_id=token).first()
                if not session:
                    return jsonify({'error': 'Invalid token'}), 401

                session_info = session.session_information
                
                login_time = datetime.fromisoformat(session_info['login_time'])
                if datetime.now() > login_time + timedelta(hours=3):
                    db.session.delete(session)
                    db.session.commit()
                    return jsonify({'error': 'Token has expired'}), 401

                current_user = None
                role = None

                if 'admin_id' in session_info:
                    current_user = Admin.query.get(session_info['admin_id'])
                    role = 'admin'
                elif 'parent_id' in session_info:
                    current_user = Parent.query.get(session_info['parent_id'])
                    role = 'parent'
                elif 'child_id' in session_info:
                    current_user = Child.query.get(session_info['child_id'])
                    role = 'child'

                if not current_user:
                    return jsonify({'error': 'User not found'}), 401

                if allowed_roles and role not in allowed_roles:
                    return jsonify({'error': 'Insufficient permissions'}), 403

                kwargs['current_user'] = current_user
                kwargs['role'] = role

                return f(*args, **kwargs)

            except SQLAlchemyError as e:
                db.session.rollback()
                return jsonify({'error': 'Database error occurred', 'details': str(e)}), 500

        return decorated
    return decorator


@api.route('/dummyData', methods=['GET'])
def dummyData():
    createDummyData()
    return "Dummy data has been created!"

@api.route('/auth/parent_register',methods=['POST'])
def parent_register():
    return parent_regisc(request)

@api.route('/auth/children_register',methods=['POST'])
def child_register():
    return child_regisc(request)

@api.route('/auth/admin_login',methods=['POST'])
def admin_login():
    return admin_loginc()

@api.route('/auth/parent_login',methods=['POST'])
def parent_login():    
    return parent_loginc(request)

@api.route('/auth/children_login', methods=['POST'])
def child_login():
    return child_loginc(request)

@api.route('/api/child/curriculum/<int:curriculum_id>/lessons', methods=['GET'])
@token_required(allowed_roles=['child'])
def get_skill_lessons_route(curriculum_id, current_user, role):
    return get_skill_lessons(current_user.child_id, curriculum_id)

@api.route('/api/child/lesson/<int:lesson_id>', methods=['GET'])
@token_required(allowed_roles=['child'])    
def get_lesson_details_route(lesson_id, current_user, role):
    return get_lesson_details(current_user.child_id, lesson_id)

@api.route('/api/child/lesson/<int:lesson_id>/mark-read', methods=['POST'])
@token_required(allowed_roles=['child'])    
def mark_lesson_complete_route(lesson_id, current_user, role):
    completed_at = request.json.get('completed_at') if request.json else None
    return mark_lesson_completed(current_user.child_id, lesson_id, completed_at)

@api.route('/api/child/lesson/<int:lesson_id>/activities', methods=['GET'])
@token_required(allowed_roles=['child'])
def get_lesson_activities_route(lesson_id, current_user, role):
    return get_lesson_activities(current_user.child_id, lesson_id)

@api.route('/api/child/activity/<int:activity_id>', methods=['GET'])
@token_required(allowed_roles=['child'])
def get_activity_details_route(activity_id, current_user, role):
    return get_activity_details(current_user.child_id, activity_id)

@api.route('/api/child/activity/<int:activity_id>/submit', methods=['POST'])
@token_required(allowed_roles=['child'])    
def submit_activity_route(activity_id, current_user, role):
    return submit_activity(current_user.child_id, activity_id)

@api.route('/api/child/activity/<int:activity_id>/history', methods=['GET'])
@token_required(allowed_roles=['child'])
def get_activity_history_route(activity_id, current_user, role):
    return get_activity_history(current_user.child_id, activity_id)

@api.route('/api/child/activity/history/<int:activity_history_id>', methods=['GET'])
@token_required(allowed_roles=['child'])
def get_activity_submission_route(activity_history_id, current_user, role):
    return get_activity_submission(current_user.child_id, activity_history_id)

@api.route('/api/child/lesson/<int:lesson_id>/quizzes', methods=['GET'])
@token_required(allowed_roles=['child'])
def get_quizzes_route(lesson_id, current_user, role):
    return get_lesson_quizzes(current_user.child_id, lesson_id)

@api.route('/api/child/curriculum/<int:curriculum_id>/lesson/<int:lesson_id>/quiz/<int:quiz_id>', methods=['GET'])
@token_required(allowed_roles=['child'])
def get_quiz_questions_route(curriculum_id, lesson_id, quiz_id, current_user, role):
    return get_quiz_questions(curriculum_id, lesson_id, quiz_id)

@api.route('/api/child/quizzes/<int:quiz_id>/submit', methods=['POST'])
@token_required(allowed_roles=['child'])
def submit_quiz_route(quiz_id, current_user, role):
    return submit_quiz(current_user.child_id, quiz_id)

@api.route('/api/child/quiz/<int:quiz_id>/history', methods=['GET'])
@token_required(allowed_roles=['child'])    
def get_quiz_history_route(quiz_id, current_user, role):
    return get_quiz_history(current_user.child_id, quiz_id)

@api.route('/api/child/setting', methods=['GET'])
@token_required(allowed_roles=['child'])
def get_child_profile_route(current_user, role):
    return get_child_profile(current_user.child_id)

@api.route('/api/child/update_profile', methods=['PUT'])
@token_required(allowed_roles=['child'])
def update_child_profile_route(current_user, role):
    return update_child_profile(current_user.child_id)

@api.route('/api/child/change_password', methods=['PUT'])
@token_required(allowed_roles=['child'])
def change_child_password_route(current_user, role):
    return change_child_password(current_user.child_id)

@api.route('/api/child/profile_image', methods=['GET','POST'])
@token_required(allowed_roles=['child'])
def child_profile_image_route(current_user, role):
    return child_profile_image(current_user.child_id)

