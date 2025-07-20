from flask import request, jsonify, send_file
from io import BytesIO
from .db import db
from .models import Admin, Session, Parent, Child, Skill, Lesson, LessonHistory, Activity, ActivityHistory, Quiz, QuizHistory, Badge, BadgeHistory
from .demoData import createDummyData
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime, date,timedelta
import uuid
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import time
import base64


from functools import wraps


def parent_regisc(request):
    # Function for parent registration that will later be sent as a request to the routes
    try:
        data=request.get_json()
        name=data.get('name')
        email=data.get('email')
        password=data.get('password')
        pic=data.get('profile_image')
        if pic == '':
            pic = None
        if not all([name,email,password]):
            return jsonify({'error':'Invalid/Missing fields'}), 400
        else:
            parent=Parent.query.filter_by(email_id=email).first()
            if parent:
                return jsonify({'error':'Email already registered'}), 409
            if len(password) < 4:
                return jsonify({
                    'status': 'error', 
                    'message': 'New password must be at least 4 characters long'
                }), 400

            hashed_password=generate_password_hash(password)
            new_parent=Parent(name=name,email_id=email,password=hashed_password,profile_image=pic)
            db.session.add(new_parent)
            db.session.commit()
            session_id = str(uuid.uuid4())
            session_info = {
                "parent_id": new_parent.parent_id,
                "email": new_parent.email_id,
                "login_time": datetime.now().isoformat()
            }
            new_session = Session(session_id=session_id, session_information=session_info)
            db.session.add(new_session)
            db.session.commit()
            return jsonify({
            "session": {
                "token": session_id,
                "login_time": session_info["login_time"]
            },
            "user": {
                "id": new_parent.parent_id
            }
        }), 201
    except Exception as e:
        print(f"Parent registration error: {e}")
        return jsonify({'error': 'Something went wrong during parent registration'}), 500

def age_calc(dob):
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    

def child_regisc(request):
    # Function for children registration that will later be sent as a request to the routes
    try:
        data=request.get_json()
        name=data.get('name')
        email=data.get('email')
        username=data.get('username')
        password=data.get('password')
        dob_str=data.get('dob')
        school=data.get('school')
        pic=data.get('profile_image')
        if pic == '':
            pic = None
        if dob_str:
            try:
                dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        else:
            dob = None
        if not all([name,username,password,dob]):
            return jsonify({'error':'Invalid/Missing fields'}), 400
        else:
            age = age_calc(dob)
            if age < 8 or age > 14:
                return jsonify({'error': 'Only children aged 8 to 14 can register'}), 400
            else:
                children=Child.query.filter_by(username=username).first()
                if children:
                    return jsonify({'error':'Username already registered'}), 409
                if email and Child.query.filter_by(email_id=email).first():
                    return jsonify({'error': 'Email already registered'}), 409
                if len(password) < 4:
                    return jsonify({
                        'status': 'error', 
                        'message': 'New password must be at least 4 characters long'
                    }), 400
                hashed_password=generate_password_hash(password)
                new_child=Child(name=name,email_id=email,username=username,password=hashed_password,dob=dob,
                                school=school,profile_image=pic)
                db.session.add(new_child)
                db.session.commit()
                session_id = str(uuid.uuid4())
                session_info = {
                    "child_id": new_child.child_id,
                    "username": new_child.username,
                    "email": new_child.email_id if email else None,
                    "login_time": datetime.now().isoformat()
                }
                new_session = Session(session_id=session_id, session_information=session_info)
                db.session.add(new_session)
                db.session.commit()
                return jsonify({
                "session": {
                    "token": session_id,
                    "login_time": session_info["login_time"]
                },
                "user": {
                    "id": new_child.child_id
                }
            }), 201
    except Exception as e:
        print(f"Registration error: {e}")  
        return jsonify({'error': 'Something went wrong during child registration'}), 500

def admin_create():
    # Function to create the admin automatically
    aemail="admin@gmail.com"
    apassword="1234"
    exist=Admin.query.filter_by(email_id=aemail).first()
    if not exist:
        hashedp=generate_password_hash(apassword)
        newa=Admin(email_id=aemail,password=hashedp)
        db.session.add(newa)
        db.session.commit()
        print("admin created")
    else:
        print("admin in database")

def admin_loginc():
    # Login function for the admin
    
    data = request.get_json()
    email = data.get('email_id')
    password = data.get('password')
    if not email or not password:
        return jsonify({"error": "Missing email or password"}), 500
    
    if len(password) < 4:
        return jsonify({
            'status': 'error', 
            'message': 'New password must be at least 4 characters long'
        }), 400

    admin = Admin.query.filter_by(email_id=email).first()
    if not admin or not check_password_hash(admin.password, password):
        return jsonify({"error": "Invalid email or password"}), 401
    
    token = str(uuid.uuid4())
    session_info = {
        "admin_id": admin.admin_id,
        "email_id": admin.email_id,
        "login_time": datetime.now().isoformat()
    }
    
    try:
        new_session = Session(session_id=token, session_information=session_info)
        db.session.add(new_session)
        db.session.commit()
        
        return jsonify({
            "session": {
                "token": token,
                "login_time": session_info["login_time"]
            },
            "user": {
                "id": admin.admin_id
            }
        }), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error occurred", "details": str(e)}), 500
    

def parent_loginc(request):
    """
    Handle parent login request by validating credentials and generating a session token.
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Missing required fields'}), 400

    parent = Parent.query.filter_by(email_id=email).first()
    if not parent or not check_password_hash(parent.password, password):
        return jsonify({'error': 'Invalid email or password'}), 401

    token = str(uuid.uuid4())
    session_info = {
        'parent_id': parent.parent_id,
        'email': parent.email_id,
        'login_time': datetime.now().isoformat()
    }

    try:
        new_session = Session(session_id=token, session_information=session_info)
        db.session.add(new_session)
        db.session.commit()

        return jsonify({
            'session': {
                'token': token,
                'login_time': session_info['login_time']
            },
            'user': {
                'id': parent.parent_id
            }
        }), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred', 'details': str(e)}), 500


def child_loginc(request):
    """
    Handle child login request by validating credentials and generating a session token.
    """
    data = request.get_json()
    identifier = data.get('email_or_username')
    password = data.get('password')

    if not identifier or not password:
        return jsonify({'error': 'Missing required fields'}), 400

    child = Child.query.filter(
        (Child.username == identifier) | (Child.email_id == identifier)
    ).first()
    if not child or not check_password_hash(child.password, password):
        return jsonify({'error': 'Invalid email or password'}), 401

    token = str(uuid.uuid4())
    session_info = {
        'child_id': child.child_id,
        'email': identifier,
        'login_time': datetime.now().isoformat()
    }

    try:
        new_session = Session(session_id=token, session_information=session_info)
        db.session.add(new_session)
        db.session.commit()

        return jsonify({
            'session': {
                'token': token,
                'login_time': session_info['login_time']
            },
            'user': {
                'id': child.child_id
            }
        }), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred', 'details': str(e)}), 500
    

# dashboard

def get_auser(current_user, role):
    # this is according to auth.md and fetches the details of users from the session id as authorisation bearer BUT it returns full profile info
    if role == "child":
        return jsonify({
            "user": {
                "id": current_user.child_id,
                "role": "child",
                "username": current_user.username,
                "email": current_user.email_id,
                "dob": current_user.dob.isoformat() if current_user.dob else None,
                "school": current_user.school,
                "profile_image": None  
            }
        }), 200
    elif role == "parent":
        return jsonify({
            "user": {
                "id": current_user.parent_id,
                "role": "parent",
                "name": current_user.name,
                "email": current_user.email_id,
                "profile_image": None  
            }
        }), 200
    elif role == "admin":
        return jsonify({
            "user": {
                "id": current_user.admin_id,
                "role": "admin",
                "email": current_user.email_id
            }
        }), 200
    return jsonify({'error': 'Invalid session data'}), 401

def get_child_dashboard_stats(current_user, role):
    # gets the stats for the child
    child_id = current_user.child_id
    lessons_completed = LessonHistory.query.filter_by(child_id=child_id).count()
    all_lessons = Lesson.query.all()
    skill_progress = {}
    for lesson in all_lessons:
        if lesson.skill_id not in skill_progress:
            skill_progress[lesson.skill_id] = []
        skill_progress[lesson.skill_id].append(lesson.lesson_id)
    completed_skills = 0
    for skill_id, lesson_ids in skill_progress.items():
        completed = LessonHistory.query.filter(
            LessonHistory.child_id == child_id,
            LessonHistory.lesson_id.in_(lesson_ids)
        ).count()
        if completed == len(lesson_ids):
            completed_skills += 1
    badges_earned = BadgeHistory.query.filter_by(child_id=child_id).count()
    child = Child.query.get(child_id)
    streak = child.streak if child else 0
    leaderboard_rank = 1  
    heatmap = [
        {"date": datetime.now().strftime('%Y-%m-%d'), "status": 1}
    ]
    return jsonify({
        "lessons_completed": lessons_completed,
        "skills_completed": completed_skills,
        "streak": streak,
        "badges_earned": badges_earned,
        "leaderboard_rank": leaderboard_rank,
        "heatmap": heatmap
    }), 200

def get_user_skill_progress(current_user, role):
    # gets the child lesson progress
    child_id = current_user.child_id
    skills = Skill.query.all()
    response = []
    for skill in skills:
        total_lessons = Lesson.query.filter_by(skill_id=skill.skill_id).count()
        completed = LessonHistory.query.join(Lesson).filter(
            Lesson.skill_id == skill.skill_id,
            LessonHistory.child_id == child_id
        ).count()
        percent = int((completed / total_lessons) * 100) if total_lessons else 0
        response.append({
            "name": skill.name,
            "link": f"/skills/{skill.skill_id}",  
            "percentage_completed": percent
        })

    return jsonify(response), 200

def get_user_badges(current_user, role):
    #  gets the child badges
    child_id = current_user.child_id
    data = db.session.query(Badge.name).join(BadgeHistory).filter(BadgeHistory.child_id == child_id).all()
    response = [{"name": name, "image": ""} for (name,) in data]
    return jsonify(response), 200

def get_curriculums_for_child(current_user, role):
    child_id = current_user.child_id
    child = current_user
    age = age_calc(child.dob)
    skills = Skill.query.filter(Skill.min_age <= age, Skill.max_age >= age).all()
    skill_ids = [s.skill_id for s in skills]
    lessons = Lesson.query.filter(Lesson.skill_id.in_(skill_ids)).all()
    lesson_ids = [l.lesson_id for l in lessons]
    lesson_map = {}
    for lesson in lessons:
        lesson_map.setdefault(lesson.skill_id, []).append(lesson.lesson_id)
    activities = Activity.query.filter(Activity.lesson_id.in_(lesson_ids)).all()
    quizzes = Quiz.query.filter(Quiz.lesson_id.in_(lesson_ids)).all()
    completed_lessons = {
        lh.lesson_id for lh in LessonHistory.query.filter(
            LessonHistory.child_id == child_id,
            LessonHistory.lesson_id.in_(lesson_ids)
        )
    }
    completed_activities = {
        ah.activity_id for ah in ActivityHistory.query.filter(
            ActivityHistory.activity_id.in_([a.activity_id for a in activities])
        )
    }
    passed_quizzes = {
        qh.quiz_id for qh in QuizHistory.query.filter(
            QuizHistory.child_id == child_id,
            QuizHistory.quiz_id.in_([q.quiz_id for q in quizzes]),
            QuizHistory.score >= 40
        )
    }
    # result
    result = []
    for skill in skills:
        lids = lesson_map.get(skill.skill_id, [])
        aids = [a.activity_id for a in activities if a.lesson_id in lids]
        qids = [q.quiz_id for q in quizzes if q.lesson_id in lids]
        total = len(lids) + len(aids) + len(qids)
        completed = (
            sum(1 for lid in lids if lid in completed_lessons) +
            sum(1 for aid in aids if aid in completed_activities) +
            sum(1 for qid in qids if qid in passed_quizzes)
        )
        progress = round((completed / total) * 100) if total else 0
        result.append({
            "curriculum_id": skill.skill_id,
            "name": skill.name,
            "description": skill.description,
            "image": None,
            "progress_status": progress
        })
    return jsonify({"curriculums": result}), 200

def get_skill_lessons(child_id, skill_id):
    try:
        skill = Skill.query.get(skill_id)

        if not skill:
            return jsonify({'error': 'Skill not found'}), 404
        
        lessons = Lesson.query.filter_by(skill_id=skill_id).order_by(Lesson.position).all()
        if not lessons:
            return jsonify({'error': 'No lessons found for this skill'}), 404
        
        
        activities = Activity.query.filter(
            Activity.lesson_id.in_([lesson.lesson_id for lesson in lessons]),
            Activity.child_id == child_id
        ).all()

        activities_by_lesson = {}
        activity_id_to_lesson_id = {}
        for activity in activities:
            activities_by_lesson.setdefault(activity.lesson_id, []).append(activity)
            activity_id_to_lesson_id[activity.activity_id] = activity.lesson_id

        activity_history = ActivityHistory.query.filter(
            ActivityHistory.activity_id.in_(activity_id_to_lesson_id.keys())
        ).all()

        attempted_activities_by_lesson = {}
        for ah in activity_history:
            lesson_id = activity_id_to_lesson_id.get(ah.activity_id)
            if lesson_id:
                attempted_activities_by_lesson.setdefault(lesson_id, set()).add(ah.activity_id)

        quizzes = Quiz.query.filter(Quiz.lesson_id.in_([lesson.lesson_id for lesson in lessons])).all()
        
        quizzes_by_lesson = {}
        quiz_id_to_lesson_id = {}
        for quiz in quizzes:
            quizzes_by_lesson.setdefault(quiz.lesson_id, []).append(quiz)
            quiz_id_to_lesson_id[quiz.quiz_id] = quiz.lesson_id

        quiz_history = QuizHistory.query.filter(
            QuizHistory.quiz_id.in_(quiz_id_to_lesson_id.keys()),
            QuizHistory.child_id == child_id
        ).all()

        attempted_quizzes_by_lesson = {}
        for qh in quiz_history:
            lesson_id = quiz_id_to_lesson_id.get(qh.quiz_id)
            if lesson_id:
                attempted_quizzes_by_lesson.setdefault(lesson_id, set()).add(qh.quiz_id)

        lessons_data = []
        for lesson in lessons:
            total_activities = len(activities_by_lesson.get(lesson.lesson_id, []))
            attempted_activities = len(attempted_activities_by_lesson.get(lesson.lesson_id, set()))
            total_quizzes = len(quizzes_by_lesson.get(lesson.lesson_id, []))
            attempted_quizzes = len(attempted_quizzes_by_lesson.get(lesson.lesson_id, set()))
            lessons_data.append({
                'lesson_id': lesson.lesson_id,
                'title': lesson.title,
                'image': lesson.image,
                'description': lesson.description,
                'progress_status': ((attempted_quizzes + attempted_activities) * 100 / (total_activities + total_quizzes)) if (total_activities + total_quizzes) > 0 else 100,
            })

        return jsonify({
            'curriculum': {
                'curriculum_id': skill.skill_id,
                'name': skill.name,
            },
            'lessons': lessons_data
        }), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred', 'details': str(e)}), 500
    

def get_lesson_details(child_id, lesson_id):
    try:
        lesson = Lesson.query.get(lesson_id)
        if not lesson:
            return jsonify({'error': 'Lesson not found'}), 404
            
        lesson_history = LessonHistory.query.filter_by(
            child_id=child_id,
            lesson_id=lesson_id
        ).first()
        
        lesson_data = {
            'lesson_id': lesson.lesson_id,
            'title': lesson.title,
            'content': lesson.content,
            'image': lesson.image,
            'completed_at': lesson_history.created_at.isoformat() if lesson_history else None
        }
        
        return jsonify(lesson_data), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred', 'details': str(e)}), 500
    

def mark_lesson_completed(child_id, lesson_id, completed_at=None):
    try:
        lesson = Lesson.query.get(lesson_id)
        if not lesson:
            return jsonify({'error': 'Lesson not found'}), 404
        
        existing_history = LessonHistory.query.filter_by(
            child_id=child_id,
            lesson_id=lesson_id
        ).first()
        
        if existing_history:
            return jsonify({'message': 'Lesson already completed'}), 200
        
        # Convert completed_at string to datetime object if provided
        if completed_at:
            if isinstance(completed_at, str):
                try:
                    # Handle ISO format with 'Z' suffix
                    if completed_at.endswith('Z'):
                        completed_at = completed_at[:-1] + '+00:00'
                    completed_at = datetime.fromisoformat(completed_at)
                except ValueError:
                    return jsonify({'error': 'Invalid date format'}), 400
        else:
            completed_at = datetime.now()
        
        new_history = LessonHistory(
            child_id=child_id,
            lesson_id=lesson_id,
            created_at=completed_at
        )
        
        db.session.add(new_history)
        db.session.commit()
        
        return jsonify({'message': 'Lesson marked as completed'}), 201
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred', 'details': str(e)}), 500
    


def get_lesson_activities(child_id, lesson_id):
    try:
        lesson = Lesson.query.get(lesson_id)
        if not lesson:
            return jsonify({'error': 'Lesson not found'}), 404
        
        skill = Skill.query.get(lesson.skill_id)
        if not skill:
            return jsonify({'error': 'Curriculum not found'}), 404
        
        activities = Activity.query.filter_by(lesson_id=lesson_id, child_id=child_id).all()
        
        activity_submissions = ActivityHistory.query.filter(
            ActivityHistory.activity_id.in_([a.activity_id for a in activities])
        ).all()
        
        completed_activities = {submission.activity_id for submission in activity_submissions}
        
        activities_data = []
        for activity in activities:
            activities_data.append({
                'activity_id': activity.activity_id,
                'name': activity.name,
                'description': activity.description,
                'image': activity.image,
                'progress_status': 100 if activity.activity_id in completed_activities else 0
            })
        
        response_data = {
            'curriculum': {
                'curriculum_id': skill.skill_id,
                'name': skill.name
            },
            'lesson': {
                'lesson_id': lesson.lesson_id,
                'title': lesson.title
            },
            'activities': activities_data
        }
        
        return jsonify(response_data), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred', 'details': str(e)}), 500


def get_activity_details(child_id, activity_id):
    try:
        activity = Activity.query.filter_by(
            activity_id=activity_id,
            child_id=child_id
        ).first()

        if not activity:
            return jsonify({'error': 'Activity not found'}), 404
        
        activity_history = ActivityHistory.query.filter_by(
            activity_id=activity_id
        ).order_by(ActivityHistory.created_at.desc()).first()
        
        activity_data = {
            'activity_id': activity.activity_id,
            'name': activity.name,
            'description': activity.description,
            'image': activity.image,
            'answer_format': activity.answer_format,
            'completed_at': activity_history.created_at.isoformat() if activity_history else None
        }
        return jsonify(activity_data), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred', 'details': str(e)}), 500


def submit_activity(child_id, activity_id):
    try:
        activity = Activity.query.filter_by(            
            activity_id=activity_id,
            child_id=child_id
        ).first()
        if not activity:
            return jsonify({'error': 'Activity not found'}), 404
        
        file_data = None
        file_extension = None
        
        # Handle multipart/form-data uploads
        if request.files and 'file' in request.files:
            uploaded_file = request.files['file']
            
            if uploaded_file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            
            file_extension = uploaded_file.filename.lower().split('.')[-1]
            file_data = uploaded_file.read()
            
        # Handle raw binary uploads (Content-Type: image/jpeg, etc.)
        elif request.content_type and request.content_type.startswith(('image/', 'application/pdf')):
            file_data = request.get_data()
            
            # Determine extension from content type
            content_type_map = {
                'image/jpeg': 'jpg',
                'image/jpg': 'jpg', 
                'image/png': 'png',
                'application/pdf': 'pdf'
            }
            file_extension = content_type_map.get(request.content_type, 'jpg')
            
        else:
            return jsonify({'error': 'No file uploaded or unsupported content type'}), 400
        
        if not file_data:
            return jsonify({'error': 'No file data received'}), 400
        
        # Check file size (10MB limit)
        max_file_size = 10 * 1024 * 1024  # 10MB in bytes
        if len(file_data) > max_file_size:
            return jsonify({'error': 'File size too large. Maximum allowed size is 10MB'}), 400
        
        # Validate file format
        allowed_extensions = ['jpg', 'jpeg', 'png', 'pdf']
        if file_extension not in allowed_extensions:
            return jsonify({'error': 'Invalid file format. Only JPG, JPEG, PNG, or PDF allowed'}), 400

        submission_time = datetime.now()

        activity_submission = ActivityHistory(
            activity_id=activity_id,
            answer=file_data,
            created_at=submission_time
        )

        db.session.add(activity_submission)
        db.session.commit()

        return jsonify({
            'activity_history_id': activity_submission.activity_history_id,
            'submitted_at': submission_time.isoformat()
        }), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred', 'details': str(e)}), 500


def get_activity_history(child_id, activity_id):
    try:
        activity = Activity.query.filter_by(            
            activity_id=activity_id,
            child_id=child_id
        ).first()
        if not activity:
            return jsonify({'error': 'Activity not found'}), 404
        
        submissions = ActivityHistory.query.filter_by(
            activity_id=activity_id
        ).order_by(ActivityHistory.created_at.desc()).all()
        
        activities_submission = []
        for submission in submissions:
            submission_data = {
                'activity_history_id': submission.activity_history_id,
                'activity_id': submission.activity_id,
                'submitted_at': submission.created_at.isoformat(),
                'feedback': submission.feedback if submission.feedback else None
            }
            activities_submission.append(submission_data)
        
        return jsonify({'activities_submission': activities_submission}), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred', 'details': str(e)}), 500


def get_activity_submission(child_id, activity_history_id):
    try:
        submission = ActivityHistory.query.get(activity_history_id)
        if not submission:
            return jsonify({'error': 'Submission not found'}), 404

        activity = Activity.query.filter_by(
            activity_id=submission.activity_id,
            child_id=child_id
        ).first()

        if not activity:
            return jsonify({'error': 'Associated activity not found'}), 404
        
        if not submission.answer:
            return jsonify({'error': 'No file found for this submission'}), 404

        # Detect file type from binary data
        file_data = submission.answer
        
        # Check file signatures (magic numbers) to determine actual file type
        if file_data.startswith(b'\xFF\xD8\xFF'):  # JPEG
            content_type = 'image/jpeg'
            file_extension = 'jpg'
        elif file_data.startswith(b'\x89PNG\r\n\x1a\n'):  # PNG
            content_type = 'image/png'
            file_extension = 'png'
        elif file_data.startswith(b'%PDF'):  # PDF
            content_type = 'application/pdf'
            file_extension = 'pdf'
        else:
            # Fallback to activity.answer_format if available
            if activity.answer_format and activity.answer_format.lower() == 'pdf':
                content_type = 'application/pdf'
                file_extension = 'pdf'
            elif activity.answer_format and activity.answer_format.lower() == 'image':
                content_type = 'image/jpeg'  # Default to JPEG for images
                file_extension = 'jpg'
            else:
                content_type = 'application/octet-stream'
                file_extension = 'bin'

        return send_file(
            BytesIO(submission.answer),
            mimetype=content_type,
            as_attachment=True,
            download_name=f'submission_{activity_history_id}.{file_extension}'
        )

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred', 'details': str(e)}), 500


def get_lesson_quizzes(child_id, lesson_id):
    try:
        lesson = Lesson.query.filter_by(lesson_id=lesson_id).first()
        if not lesson:
            return jsonify({'error': 'Lesson not found or does not belong to the curriculum'}), 404
        
        skill = Skill.query.filter_by(skill_id=lesson.skill_id).first()
        if not skill:
            return jsonify({'error': 'Curriculum not found'}), 404
        
        quizzes = Quiz.query.filter_by(lesson_id=lesson_id).all()
        
        quiz_history = QuizHistory.query.filter(
            QuizHistory.quiz_id.in_([quiz.quiz_id for quiz in quizzes]),
            QuizHistory.child_id == child_id
        ).all()
        
        attempted_quizzes = {history.quiz_id for history in quiz_history}
        
        quizzes_data = []
        for quiz in quizzes:
            quizzes_data.append({
                'quiz_id': quiz.quiz_id,
                'name': quiz.quiz_name,
                'description': quiz.description,
                'time_duration': quiz.time_duration,
                'progress_status': 100 if quiz.quiz_id in attempted_quizzes else 0,
                'image': quiz.image
            })
        
        response_data = {
            'curriculum': {
                'curriculum_id': skill.skill_id,
                'name': skill.name
            },
            'lesson': {
                'lesson_id': lesson.lesson_id,
                'title': lesson.title
            },
            'quizzes': quizzes_data
        }
        
        return jsonify(response_data), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred', 'details': str(e)}), 500

def get_quiz_history(child_id, quiz_id):
    try:
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return jsonify({'error': 'Quiz not found'}), 404
        
        quiz_attempts = QuizHistory.query.filter_by(
            child_id=child_id,
            quiz_id=quiz_id
        ).order_by(QuizHistory.created_at.desc()).all()
        
        quizzes_history = []
        for attempt in quiz_attempts:
            quizzes_history.append({
                'quiz_history_id': attempt.quiz_history_id,
                'quiz_id': attempt.quiz_id,
                'attempted_at': attempt.created_at.isoformat(),
                'score': attempt.score,
                'feedback': attempt.feedback if attempt.feedback else None
            })
        
        return jsonify({'quizzes_history': quizzes_history}), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred', 'details': str(e)}), 500


def get_quiz_questions(curriculum_id, lesson_id, quiz_id):

    try:
        # Validate curriculum exists
        curriculum = Skill.query.get(curriculum_id)
        if not curriculum:
            return jsonify({'error': 'Curriculum not found'}), 404
        
        # Validate lesson exists and belongs to curriculum
        lesson = Lesson.query.filter_by(
            lesson_id=lesson_id, 
            skill_id=curriculum_id
        ).first()
        if not lesson:
            return jsonify({'error': 'Lesson not found or does not belong to the curriculum'}), 404
        
        # Validate quiz exists and belongs to lesson
        quiz = Quiz.query.filter_by(
            quiz_id=quiz_id,
            lesson_id=lesson_id
        ).first()
        if not quiz:
            return jsonify({'error': 'Quiz not found or does not belong to the lesson'}), 404
        
        # Format questions with index
        questions_data = []
        if quiz.questions:  # questions is stored as JSON
            for idx, question in enumerate(quiz.questions):
                question_data = {
                    'question_index': idx + 1,
                    'question': question.get('question', ''),
                    'options': question.get('options', []),
                    'marks': question.get('marks', 1),
                }
                questions_data.append(question_data)
        
        response_data = {
            'curriculum': {
                'curriculum_id': curriculum.skill_id,
                'name': curriculum.name
            },
            'lesson': {
                'lesson_id': lesson.lesson_id,
                'title': lesson.title
            },
            'quizzes': {
                'quiz_id': quiz.quiz_id,
                'name': quiz.quiz_name,
                'time_duration': quiz.time_duration
            },
            'questions': questions_data
        }
        
        return jsonify(response_data), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred', 'details': str(e)}), 500


def submit_quiz(child_id, quiz_id):
    """
    Submit quiz answers and calculate score.
    Expected format: {"answers": {"question_index": "option_index"}}
    Questions and answers arrays have the same order by index.
    """
    try:
            
        # Validate quiz exists
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return jsonify({'error': 'Quiz not found'}), 404
        
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        answers = data.get('answers')
        if not answers or not isinstance(answers, dict):
            return jsonify({'error': 'Invalid answers format. Expected dictionary with question_index: option_index'}), 400
        
        # Validate quiz has questions and answers
        if not quiz.questions or not quiz.answers:
            return jsonify({'error': 'Quiz has no questions or answer key'}), 500
        
        # Validate questions and answers arrays have same length
        if len(quiz.questions) != len(quiz.answers):
            return jsonify({'error': 'Quiz data inconsistency: questions and answers count mismatch'}), 500
        
        score = 0
        total_questions = len(quiz.questions)
        total_score = sum(q.get('marks', 1) for q in quiz.questions)
        
        # Process each submitted answer
        for question_index_str, option_index_str in answers.items():
            try:
                question_index = int(question_index_str)
                option_index = int(option_index_str)
            except (ValueError, TypeError):
                continue  
            
            # Validate question index (1-based indexing)
            if question_index < 1 or question_index > total_questions:
                continue  
            
            array_index = question_index - 1
            
            question_data = quiz.questions[array_index]
            answer_data = quiz.answers[array_index]
            
            options = question_data.get('options', [])
            question_marks = question_data.get('marks', 1)
            correct_answer = answer_data.get('correct_answer', '')
            
            # Validate option index (0-based indexing)
            if option_index < 0 or option_index >= len(options):
                continue  # Skip invalid option index
            
            # Get selected option
            selected_option = options[option_index]
            
            # Extract option text (handle both string and dict formats)
            if isinstance(selected_option, dict):
                selected_option_text = selected_option.get('text', '')
            elif isinstance(selected_option, str):
                selected_option_text = selected_option
            else:
                selected_option_text = str(selected_option)
            
            # Check if selected option is correct (single correct answer)
            if selected_option_text == correct_answer:
                score += question_marks
        
        # Save quiz attempt to history
        quiz_history = QuizHistory(
            child_id=child_id,
            quiz_id=quiz_id,
            score=score,
            created_at=datetime.now()
        )
        
        db.session.add(quiz_history)
        db.session.commit()
        
        return jsonify({
            'score': score,
            'total_score': total_score
        }), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred', 'details': str(e)}), 500
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


def get_child_profile(child_id):
    try:
        child = Child.query.get(child_id)
        if not child:
            return jsonify({'error': 'Child not found'}), 404
        
        profile_data = {
            'profile_image_url': child.profile_image if child.profile_image else '',
            'name': child.name,
            'dob': child.dob.isoformat() if child.dob else None,
            'email': child.email_id,
            'school': child.school
        }
        
        return jsonify(profile_data), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred', 'details': str(e)}), 500


def update_child_profile(child_id):
    try:
        child = Child.query.get(child_id)
        if not child:
            return jsonify({'error': 'Child not found'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Check if at least one field is provided
        allowed_fields = ['name', 'email', 'dob', 'school']
        if not any(field in data for field in allowed_fields):
            return jsonify({'error': 'At least one field must be provided'}), 400
        
        # Update name if provided
        if 'name' in data:
            if not data['name'] or not data['name'].strip():
                return jsonify({'error': 'Name cannot be empty'}), 400
            child.name = data['name'].strip()
        
        # Update email if provided
        if 'email' in data:
            email = data['email']
            if email:  # If email is not empty, validate it
                # Check if email is already taken by another child
                existing_child = Child.query.filter(
                    Child.email_id == email,
                    Child.child_id != child_id
                ).first()
                if existing_child:
                    return jsonify({'error': 'Email already registered by another child'}), 409
                child.email_id = email
            else:
                child.email_id = None  # Allow setting email to null
        
        # Update date of birth if provided
        if 'dob' in data:
            dob_str = data['dob']
            if dob_str:
                try:
                    dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
                    # Validate age (8-14 years old)
                    age = age_calc(dob)
                    if age < 8 or age > 14:
                        return jsonify({'error': 'Child must be between 8 and 14 years old'}), 400
                    child.dob = dob
                except ValueError:
                    return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
            else:
                return jsonify({'error': 'Date of birth cannot be empty'}), 400
        
        # Update school if provided
        if 'school' in data:
            child.school = data['school']  # Allow school to be empty/null
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Profile details updated'
        }), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred', 'details': str(e)}), 500


def change_child_password(child_id):
    try:
        child = Child.query.get(child_id)
        if not child:
            return jsonify({'status': 'error', 'message': 'Child not found'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'status': 'error', 'message': 'No data provided'}), 400
        
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')
        
        # Validate required fields
        if not all([current_password, new_password, confirm_password]):
            return jsonify({
                'status': 'error', 
                'message': 'Current password, new password, and confirm password are required'
            }), 400
        
        # Verify current password
        if not check_password_hash(child.password, current_password):
            return jsonify({
                'status': 'error', 
                'message': 'Current password is incorrect'
            }), 400
        
        # Validate new password matches confirm password
        if new_password != confirm_password:
            return jsonify({
                'status': 'error', 
                'message': 'New password and confirm password do not match'
            }), 400
        
        # Validate new password length (optional - add your own requirements)
        if len(new_password) < 4:
            return jsonify({
                'status': 'error', 
                'message': 'New password must be at least 4 characters long'
            }), 400
        
        # Ensure new password is different from current password
        if check_password_hash(child.password, new_password):
            return jsonify({
                'status': 'error', 
                'message': 'New password must be different from current password'
            }), 400
        
        # Hash and update the new password
        child.password = generate_password_hash(new_password)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Password changed successfully'
        }), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': 'Database error occurred'}), 500



def child_profile_image(child_id):
    """
    Handle both GET and POST requests for child profile images.
    GET: Retrieve profile image
    POST: Upload/update profile image
    """
    try:
        # Find the child
        child = Child.query.get(child_id)
        
        if request.method == 'POST':
            data=request.get_json()
            pic= data.get('profile_image') if (data.get('profile_image') != '') else None
            
            child.profile_image = pic
            db.session.commit()

        elif request.method == 'GET':
            return jsonify({
                'profile_image': child.profile_image if child.profile_image else '',
            }), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': 'Database error occurred'}), 500
    



