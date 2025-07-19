import json
from flask import request, jsonify
from .db import db
from .models import Admin, Session, Parent, Child, Skill, Lesson, LessonHistory, Activity, ActivityHistory, Quiz, QuizHistory, Badge, BadgeHistory
from .demoData import createDummyData
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime, date
import uuid
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import time
import base64
from .decorators import only_admin, only_parent, only_admin_or_parent

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

def get_auser():
    # this is according to auth.md and fetches the details of users from the session id as authorisation bearer BUT it returns full profile info
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({'error': 'Missing or malformed token'}), 403
    token = auth_header.split(" ")[1]
    session = Session.query.filter_by(session_id=token).first()
    if not session:
        return jsonify({'error': 'Invalid credentials'}), 401
    info = session.session_information
    if "child_id" in info:
        child = Child.query.get(info["child_id"])
        if not child:
            return jsonify({'error': 'User not found'}), 404
        return jsonify({
            "user": {
                "id": child.child_id,
                "role": "child",
                "username": child.username,
                "email": child.email_id,
                "dob": child.dob.isoformat() if child.dob else None,
                "school": child.school,
                "profile_image": None  
            }
        }), 200
    elif "parent_id" in info:
        parent = Parent.query.get(info["parent_id"])
        if not parent:
            return jsonify({'error': 'User not found'}), 404
        return jsonify({
            "user": {
                "id": parent.parent_id,
                "role": "parent",
                "name": parent.name,
                "email": parent.email_id,
                "profile_image": None  
            }
        }), 200
    return jsonify({'error': 'Invalid session data'}), 401


# def fetch_user_details(request):
#     # this is accr to dashboard.md and fetches the minor details of students returns half info
#     auth_header = request.headers.get('Authorization')
#     if not auth_header or not auth_header.startswith("Bearer "):
#         return jsonify({'error': 'Missing or malformed token'}), 403
#     token = auth_header.split(" ")[1]
#     session = Session.query.filter_by(session_id=token).first()
#     if not session:
#         return jsonify({'error': 'Invalid credentials'}), 401
#     session_info = session.session_information
#     user_id = session_info.get('parent_id') or session_info.get('child_id') 
#     if 'parent_id' in session_info:
#         user_type = 'parent'
#         user = Parent.query.get(user_id)
#         name = user.name
#         email = user.email_id
#     elif 'child_id' in session_info:
#         user_type = 'child'
#         user = Child.query.get(user_id)
#         name = user.name
#         email = user.email_id or ''  
#     else:
#         return jsonify({'error': 'User not recognized'}), 401
#     return jsonify({
#         "name": name,
#         "email": email,
#         "id": user_id,
#         "user_type": user_type
#     }), 200


def get_child_dashboard_stats(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({'error': 'Missing or malformed token'}), 403
    token = auth_header.split(" ")[1]
    session = Session.query.filter_by(session_id=token).first()
    if not session or 'child_id' not in session.session_information:
        return jsonify({'error': 'Invalid or unauthorized session'}), 401
    child_id = session.session_information['child_id']
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
    leaderboard_rank = 1  # gotta to implement logic will discuss in meeting
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

def get_user_skill_progress(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({'error': 'Missing or malformed token'}), 403
    token = auth_header.split(" ")[1]
    session = Session.query.filter_by(session_id=token).first()
    if not session or 'child_id' not in session.session_information:
        return jsonify({'error': 'Invalid or unauthorized session'}), 401
    child_id = session.session_information['child_id']
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
            "link": f"/skills/{skill.skill_id}",  # gotta discuss with frontend about this url
            "percentage_completed": percent
        })

    return jsonify(response), 200


def get_user_badges():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({'error': 'Missing or malformed token'}), 403
    token = auth_header.split(" ")[1]
    session = Session.query.filter_by(session_id=token).first()
    if not session or 'child_id' not in session.session_information:
        return jsonify({'error': 'Unauthorized'}), 401
    child_id = session.session_information['child_id']
    badge_histories = BadgeHistory.query.filter_by(child_id=child_id).all()
    response = []
    for bh in badge_histories:
        badge = Badge.query.get(bh.badge_id)
        if badge:
            response.append({
                "name": badge.name,
                "image": ""  # gotta add this 
            })
    return jsonify(response), 200

def get_lesson_quizzes(child_id, curriculum_id, lesson_id):
    # Get curriculum(Skill)
    curriculum = Skill.query.get(curriculum_id)
    if not curriculum:
        return jsonify({'error': 'Curriculum not found'}), 404
    #G et lesson 
    lesson = Lesson.query.filter_by(lesson_id=lesson_id, skill_id=curriculum_id).first()
    if not lesson:
        return jsonify({'error': 'Lesson not found'}), 404
    quizzes = Quiz.query.filter_by(lesson_id=lesson_id).all()
    attempted_quiz_ids = {
        qh.quiz_id for qh in QuizHistory.query.filter_by(child_id=child_id).all()
    }
    quiz_list = []
    for quiz in quizzes:
        quiz_data = {
            "quiz_id": quiz.quiz_id,
            "name": quiz.quiz_name,
            "description": quiz.description,
            "time_duration": f"{quiz.time_duration // 60} mins" if quiz.time_duration else "N/A",
            "difficulty": "Medium",  
            "progress_status": 100 if quiz.quiz_id in attempted_quiz_ids else 0,
            "image": None  
        }
        quiz_list.append(quiz_data)
    return jsonify({
        "curriculum": {
            "curriculum_id": curriculum.skill_id,
            "name": curriculum.name
        },
        "lesson": {
            "lesson_id": lesson.lesson_id,
            "title": lesson.title
        },
        "quizzes": quiz_list
    }), 200


def get_quiz_history(child_id, quiz_id):
    # Get teh quiz history
    histories = QuizHistory.query.filter_by(child_id=child_id, quiz_id=quiz_id).all()
    if not histories:
        return jsonify({"quizzes_history": []}), 200
    child = Child.query.get(child_id)
    parent_name = child.parent.name if child.parent else None
    parent_email = child.parent.email_id if child.parent else None
    history_list = []
    for h in histories:
        history_list.append({
            "quiz_history_id": h.quiz_history_id,
            "quiz_id": h.quiz_id,
            "attempted_at": h.created_at.isoformat() if hasattr(h, "created_at") else "N/A",
            "score": h.score,
            "feedback": {
                "admin": "admin@gmail.com",  
                "parent": f"Parent: {parent_name} ({parent_email})" if parent_name else ""
            }
        })
    return jsonify({"quizzes_history": history_list}), 200


def get_curriculums_for_child(child_id):
    # Get skills
    child = Child.query.get(child_id)
    if not child:
        return jsonify({"error": "Child not found"}), 404
    age = age_calc(child.dob)
    skills = Skill.query.filter(Skill.min_age <= age, Skill.max_age >= age).all()
    result = []
    for skill in skills:
        # Lessons, Activities, Quizzes under this skill
        lessons = Lesson.query.filter_by(skill_id=skill.skill_id).all()
        lesson_ids = [l.lesson_id for l in lessons]
        activities = Activity.query.filter(Activity.lesson_id.in_(lesson_ids)).all()
        activity_ids = [a.activity_id for a in activities]
        quizzes = Quiz.query.filter(Quiz.lesson_id.in_(lesson_ids)).all()
        quiz_ids = [q.quiz_id for q in quizzes]
        total_items = len(lesson_ids) + len(activity_ids) + len(quiz_ids)
        completed_lessons = LessonHistory.query.filter(
            LessonHistory.child_id == child_id,
            LessonHistory.lesson_id.in_(lesson_ids)
        ).count()
        submitted_activities = ActivityHistory.query.filter(
            ActivityHistory.activity_id.in_(activity_ids)
        ).count()
        passed_quizzes = QuizHistory.query.filter(
            QuizHistory.child_id == child_id,
            QuizHistory.quiz_id.in_(quiz_ids),
            QuizHistory.score >= 40  # as per iitm
        ).count()
        completed_items = completed_lessons + submitted_activities + passed_quizzes
        progress = round((completed_items / total_items) * 100) if total_items else 0
        result.append({
            "curriculum_id": skill.skill_id,
            "name": skill.name,
            "description": skill.description,
            "image": None,
            "progress_status": progress
        })
    return jsonify({"curriculums": result}), 200

@only_admin_or_parent
def get_children(session_info):
    if "admin_id" in session_info:
        children = Child.query.all()
    elif "parent_id" in session_info:
        children = Child.query.filter_by(parent_id=session_info["parent_id"]).all()
    else:
        return jsonify({"error": "Forbidden"}), 403

    response = []
    for child in children:
        response.append({
            "id": child.child_id,
            "name": child.name,
            "email": child.email_id,
            "age": age_calc(child.dob),
            "school_name": child.school,
            "last_login": child.last_login.isoformat() if child.last_login else None,
        })

    return jsonify(response), 200

@only_admin_or_parent
def get_lessons(session_info):
    lessons = Lesson.query.all()
    response = []
    for lesson in lessons:
        response.append({
            'id': lesson.lesson_id,
            'title': lesson.title,
            'curriculum': lesson.skill.name if lesson.skill else None
        })

    return jsonify(response)

@only_admin_or_parent
def get_quizzes(session_info):
    lesson_id = request.args.get('lesson_id', type=int)

    query = Quiz.query
    if lesson_id is not None:
        query = query.filter_by(lesson_id=lesson_id)

    quizzes = query.all()
    result = []
    for quiz in quizzes:
        lesson = quiz.lesson
        skill = lesson.skill if lesson else None
        result.append({
            "id": quiz.quiz_id,
            "title": quiz.quiz_name,
            "lesson": lesson.title if lesson else None,
            "curriculum": skill.name if skill else None
        })

    return jsonify(result)

@only_admin_or_parent
def get_activities(session_info):
    lesson_id = request.args.get('lesson_id', type=int)

    query = Activity.query
    if lesson_id is not None:
        query = query.filter_by(lesson_id=lesson_id)

    activities = query.all()

    response = []
    for activity in activities:
        lesson = activity.lesson
        skill = lesson.skill if lesson else None

        response.append({
            'id': activity.activity_id,
            'title': activity.name,
            'lesson': lesson.title if lesson else None,
            'curriculum': skill.name if skill else None
        })

    return jsonify(response)

BADGE_IMAGE_BASE_URL = "/home/ektabansal/soft-engg-project-may-2025-se-May-9/frontend/public/badges"

@only_admin_or_parent
def get_badges(session_info):
    badges = Badge.query.all()
    response = []
    for badge in badges:
        image_url = f"{BADGE_IMAGE_BASE_URL}{badge.badge_id}.png"

        response.append({
            "id": badge.badge_id,
            "label": badge.name,
            "image": image_url
        })

    return jsonify(response)

@only_parent 
def create_child(session_info):
    data = request.get_json()
    required_fields = ["name", "username", "password", "dob", "school"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    name = data["name"]
    username = data["username"]
    password = data["password"]
    dob_str = data["dob"]
    school = data["school"]
    pic=data.get('profile_image')
    if pic == '':
        pic = None

    try:
        dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Invalid DOB format. Expected YYYY-MM-DD."}), 400
    
    if Child.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 409
    age = age_calc(dob)
    if age < 8 or age > 14:
        return jsonify({'error': 'Only children aged 8 to 14 can register'}), 400
    else:
        children=Child.query.filter_by(username=username).first()
        if children:
            return jsonify({'error':'Username already registered'}), 409

    hashed_password=generate_password_hash(password)
    new_child = Child(
        name=name,
        username=username,
        password=hashed_password,  
        dob=dob,
        school=school,
        parent_id=session_info['parent_id'],
        profile_image=pic  
    )

    db.session.add(new_child)
    db.session.commit()

    return jsonify({
        "id": new_child.child_id,
        "name": new_child.name,
        "username": new_child.username,
        "dob": new_child.dob.isoformat(),
        "school": new_child.school,
    }), 201
 
@only_admin   
def get_parents():
    parents = Parent.query.all()

    response = []
    for parent in parents:
        response.append({
            "id": parent.parent_id,
            "name": parent.name,
            "email": parent.email_id,
            "blocked": parent.is_blocked
        })

    return jsonify(response), 200

@only_admin
def create_badge(session_info):
    data = request.get_json()
    name = data.get("title")
    description = data.get("description", "")
    image_base64 = data.get("image")

    if not name or not image_base64:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        if image_base64:
            image_binary = base64.b64decode(image_base64)
        else:
            image_binary = None
    except Exception:
        return jsonify({"error": "Invalid base64 image"}), 400

    badge = Badge(
        name=name,
        description=description,
        image=image_binary
    )

    db.session.add(badge)
    db.session.commit()

    return jsonify({
        "id": badge.badge_id,
        "label": badge.name,
        "image": badge.image,
        "description":badge.description
    }), 201

@only_admin_or_parent
def create_activity(session_info):
    lesson_id = request.args.get('lesson_id', type=int)
    data = request.get_json()
    required_fields = ['title','description','image','instructions','difficulty', 'answer_format']
    
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    title = data['title']
    description = data['description']
    image = data['image']
    instructions=data['instructions']
    difficulty=data['difficulty']    
    answer_format = data['answer_format']

    try:
        if image:
            image_base64 = base64.b64decode(image)
        else:
            image_base64 = None
    except Exception:
        return jsonify({"error": "Invalid base64 image"}), 400
    allowed_formats = ['text', 'image', 'pdf']
    if answer_format not in allowed_formats:
        return jsonify({"error": "Invalid answer_format. Must be one of: text, image, pdf"}), 400

    activity = Activity(
        name = title,
        description = description,
        instructions = instructions,
        difficulty = difficulty,
        image = image_base64,
        lesson_id = lesson_id,
        answer_format = answer_format
    )
    db.session.add(activity)
    db.session.commit()

    return jsonify({
        "id": activity.activity_id,
        "title": activity.name,
        "answer_format": activity.answer_format,
        "difficulty" : activity.difficulty
    }), 201

@only_admin  
def create_lesson(session_info):
    skill_id = request.args.get('skill_id', type=int)
    try:
        data = request.get_json()
    except Exception:
        return jsonify({'error': 'Invalid JSON'}), 400

    required = ['title', 'content', 'image']
    if not all(k in data for k in required):
        return jsonify({'error': 'Missing required fields'}), 400

    title = data['title']
    content_raw = data['content']
    image_base64 = data['image']

    skill = Skill.query.get(skill_id)
    if not skill:
        return jsonify({'error': 'Invalid curriculum_id'}), 404

    try:
        content = json.loads(content_raw) if isinstance(content_raw, str) else content_raw
    except json.JSONDecodeError:
        return jsonify({'error': 'Content must be valid JSON'}), 400

    try:
        if image_base64:
            image_binary = base64.b64decode(image_base64)
        else:
            image_binary = None
    except Exception:
        return jsonify({'error': 'Invalid base64 image'}), 400

    max_position = db.session.query(db.func.max(Lesson.position)).filter_by(skill_id=skill_id).scalar()
    next_position = (max_position or 0) + 1

    lesson = Lesson(
        skill_id=skill_id,
        title=title,
        content=content,
        image=image_binary,
        position=next_position
    )

    db.session.add(lesson)
    db.session.commit()

    return jsonify({
        "id": lesson.lesson_id,
        "title": lesson.title,
        "curriculum": skill.name,
        "position": lesson.position
    }), 201
    

@only_admin
def create_quiz(session_info):
    lesson_id = request.args.get('lesson_id', type=int)
    
    try:
        data = request.get_json()
    except Exception:
        return jsonify({'error': 'Invalid JSON format'}), 400

    required_fields = ['title','image','description', 'difficulty', 'time_duration','point', 'questions']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    picture = data['image']
    title = data['title']
    description = data['description']
    difficulty = data['difficulty']
    points = data['point']
    time_duration = data['time_duration']
    questions = data['questions']

    try:
        if picture:
            image_binary = base64.b64decode(picture)
        else:
            image_binary = None
    except Exception:
        return jsonify({'error': 'Invalid base64 image'}), 400

    if not isinstance(questions, list) or not questions:
        return jsonify({'error': 'questions must be a non-empty list'}), 400

    questions_json = []
    answers_json = []

    for idx, question in enumerate(questions):
        q_text = question.get('question')
        opts = question.get('options', [])

        if not q_text or not isinstance(opts, list) or not opts:
            return jsonify({'error': f"Invalid format in question #{idx + 1}"}), 400

        # Preserve question
        questions_json.append({
            "question": q_text,
            "options": opts
        })

        correct_answers = [opt['text'] for opt in opts if opt.get('isCorrect') is True]

        if not correct_answers:
            return jsonify({"error": f"No correct answer specified for question '{q_text}'"}), 400

        answers_json.append({
            "question": q_text,
            "correct_answers": correct_answers
        })

    max_position = db.session.query(db.func.max(Quiz.position)).filter_by(lesson_id=lesson_id).scalar()
    next_position = (max_position or 0) + 1

    quiz = Quiz(
        quiz_name=title,
        description=description,
        questions=questions_json,
        answers = answers_json,
        difficulty=difficulty,
        points=points,
        image=image_binary,
        lesson_id=lesson_id,
        position=next_position,
        is_visible=True,
        created_at=datetime.utcnow(),
        time_duration=time_duration
    )

    db.session.add(quiz)
    db.session.commit()

    return jsonify({
        "id": quiz.quiz_id,
        "title": quiz.quiz_name,
        "difficulty": quiz.difficulty,
        "points": quiz.points
    }), 201
    
    
@only_admin_or_parent
def get_child_profile(session_info):
    child_id = request.args.get('id', type=int)
    if not child_id:
        return jsonify({'error': 'Child ID is required as query param ?id=<number>'}), 400

    child = Child.query.get(child_id)
    if not child:
        return jsonify({'error': 'Child not found'}), 404

    if 'parent_id' in session_info and child.parent_id != session_info['parent_id']:
        return jsonify({'error': 'Access denied to this child profile'}), 403

    today = datetime.today()
    age = today.year - child.dob.year - ((today.month, today.day) < (child.dob.month, child.dob.day))
    parent = Parent.query.get(child.parent_id)

    skills_progress = []
    all_skills = Skill.query.all()
    for skill in all_skills:
        lessons = Lesson.query.filter_by(skill_id=skill.skill_id).all()
        lesson_ids = [l.lesson_id for l in lessons]
        lesson_started_count = len(lesson_ids)

        lesson_completed_count = LessonHistory.query.filter(
            LessonHistory.child_id == child_id,
            LessonHistory.lesson_id.in_(lesson_ids)
        ).count()
        quiz_attempted_count = QuizHistory.query.join(Quiz).filter(
            Quiz.lesson_id.in_(lesson_ids),
            QuizHistory.child_id == child_id
        ).count()

        skills_progress.append({
            "skill_id": str(skill.skill_id),
            "skill_name": skill.name,
            "lesson_started_count": lesson_started_count,
            "lesson_completed_count": lesson_completed_count,
            "quiz_attempted_count": quiz_attempted_count
        })

    point_earned = []

    quiz_points = QuizHistory.query.filter_by(child_id=child_id).all()
    for qp in quiz_points:
        point_earned.append({
            "point": qp.score,
            "date": qp.quiz.created_at.strftime("%Y-%m-%d") if qp.quiz and qp.quiz.created_at else "N/A"
        })

    quizzes = QuizHistory.query.filter_by(child_id=child_id).all()
    assessments = []
    for qh in quizzes:
        quiz = Quiz.query.get(qh.quiz_id)
        assessments.append({
            "id": qh.quiz_history_id,
            "skill_id": str(quiz.lesson.skill_id),
            "assessment_type": "Quiz",
            "title": quiz.quiz_name,
            "date": quiz.created_at.strftime("%Y-%m-%d") if quiz.created_at else "N/A",
            "score": qh.score,
            "max_score": 100  # or make dynamic if needed
        })

    activity_histories = ActivityHistory.query.join(Activity).filter(Activity.child_id == child_id).all()
    for ah in activity_histories:
        activity = ah.activity
        assessments.append({
            "id": ah.activity_history_id,
            "skill_id": str(activity.lesson.skill_id) if activity.lesson else "N/A",
            "assessment_type": "Activity",
            "title": activity.name,
            "date": "N/A",  # You can add created_at to Activity if you want
            "score": "Pass",  # assumption — no scoring system for activity
            "max_score": "Pass"
        })

    badge_history = BadgeHistory.query.filter_by(child_id=child_id).all()
    badges = []
    for bh in badge_history:
        badge = Badge.query.get(bh.badge_id)
        if badge:
            badges.append({
                "badge_id": str(badge.badge_id),
                "title": badge.name,
                "image": "",  # Convert to base64 or use a badge URL if available
                "awarded_on": bh.awarded_on  # Placeholder (add award date if available)
            })

    return jsonify({
        "info": {
            "child_id": str(child.child_id),
            "full_name": child.name,
            "age": age,
            "enrollment_date": child.enrollment_date,
            "status": "Blocked" if child.is_blocked else "Active",
            "parent": {
                "id": parent.parent_id,
                "name": parent.name,
                "email": parent.email_id
            }
        },
        "skills_progress": skills_progress,
        "point_earned": point_earned,
        "assessments": sorted(assessments, key=lambda a: a.get("date"), reverse=True),
        "achievements": {
            "badges": badges,
            "streak": child.streak
        }
    }), 200
