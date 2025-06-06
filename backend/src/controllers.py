from flask import request, jsonify
from .db import db
from .models import Admin, Session, Parent, Child, Skill, Lesson, LessonHistory, Activity, ActivityHistory, Quiz, QuizHistory, Badge, BadgeHistory
from .demoData import createDummyData
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
import uuid
from sqlalchemy.exc import IntegrityError
import hashlib, time, random, string


def parent_regisc(request):
    # Function for parent registration that will later be sent as a request to the routes
    data=request.get_json()
    name=data.get('name')
    email=data.get('email_id')
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
        # return jsonify({'message':'Parent Registered'}), 201
        session_id = str(uuid.uuid4())
        session_info = {
            "parent_id": new_parent.parent_id,
            "email_id": new_parent.email_id,
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
    

def child_regisc(request):
    # Function for children registration that will later be sent as a request to the routes
    data=request.get_json()
    name=data.get('name')
    email=data.get('email_id')
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
        children=Child.query.filter_by(username=username).first()
        if children:
            return jsonify({'error':'Username already registered'}), 409
        hashed_password=generate_password_hash(password)
        new_child=Child(name=name,email_id=email,username=username,password=hashed_password,dob=dob,
                        school=school,profile_image=pic)
        db.session.add(new_child)
        db.session.commit()
        # return jsonify({'message':'Child Registered'}), 201
        session_id = str(uuid.uuid4())
        session_info = {
            "child_id": new_child.child_id,
            # "name":new_child.name,
            "username": new_child.username,
            # "dob":new_child.dob,
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
    aemail = data.get('email_id')
    apassword = data.get('password')
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

        return jsonify({"message": "Login successful", "session_id": session_id}), 201
    else:
        return jsonify({"error": "Invalid credentials"}), 401


        return jsonify({'message':'Child Registered'}), 201
    
def generate_custom_token(email):
    """
    Generate a secure custom token using the user's email, current timestamp, and a random string.
    """
    timestamp = str(time.time())
    random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    raw_token = email + timestamp + random_str
    return hashlib.sha256(raw_token.encode()).hexdigest()

def parent_loginc(request):
    """
    Handle parent login request by validating credentials and generating a session token.

    Args:
        request (flask.Request): The incoming HTTP request object containing JSON data.

    Returns:
        flask.Response: A JSON response with one of the following:
            - 400 status code if required fields are missing.
            - 401 status code if credentials are invalid.
            - 200 status code with session token and parent ID upon successful login.
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Missing required fields'}), 400

    parent = Parent.query.filter_by(email_id=email).first()
    if not parent or not check_password_hash(parent.password, password):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    token = generate_custom_token(email)

    session_info = {
        'parent_id': str(parent.parent_id),
        'email': parent.email_id,
        'login_time': datetime.now().isoformat()
    }

    new_session = Session(session_id=token, session_information=session_info)
    db.session.add(new_session)
    db.session.commit()

    return jsonify({
        'session': {
            'token': token,
            'login_time': session_info['login_time']
        },
        'user': {
            'id': str(parent.parent_id)
        }
    }), 200
    
def child_loginc(request):
    """
    Handle child login request by validating credentials and generating a session token.

    Args:
        request (flask.Request): The incoming HTTP request object containing JSON data.

    Returns:
        flask.Response: A JSON response with one of the following:
            - 400 status code if required fields are missing.
            - 401 status code if credentials are invalid.
            - 200 status code with session token and parent ID upon successful login.
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

    token = generate_custom_token(identifier)

    session_info = {
        'parent_id': str(child.child_id),
        'email': identifier,
        'login_time': datetime.now().isoformat()
    }

    new_session = Session(session_id=token, session_information=session_info)
    db.session.add(new_session)
    db.session.commit()

    return jsonify({
        'session': {
            'token': token,
            'login_time': session_info['login_time']
        },
        'user': {
            'id': str(child.child_id)
        }
    }), 200
