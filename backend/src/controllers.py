from flask import request, jsonify
from .db import db
from .models import Admin, Session, Parent, Child, Skill, Lesson, LessonHistory, Activity, ActivityHistory, Quiz, QuizHistory, Badge, BadgeHistory
from .demoData import createDummyData
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime, date
import uuid
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import time

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
    try:
        data = request.get_json()
        aemail = data.get('email_id')
        apassword = data.get('password')
        if not aemail or not apassword:
            return jsonify({"error": "Missing email or password"}), 500
        admin = Admin.query.filter_by(email_id=aemail).first()
        if admin and check_password_hash(admin.password, apassword):
            session_id = str(uuid.uuid4())
            sdata = {
                "admin_id": admin.admin_id,
                "email_id": admin.email_id,
                "login_time": datetime.now().isoformat()
            }
            new_session = Session(session_id=session_id, session_information=sdata)
            db.session.add(new_session)
            db.session.commit()

            return jsonify({"message": "Login successful", 
                            "session": {
                                "token": session_id,
                                "login_time": sdata["login_time"]
                },}), 201
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        print(f"Admin login error: {e}")
        return jsonify({"error": "Something went wrong during login"}), 500    

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
