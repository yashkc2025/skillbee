from flask import request, jsonify
from .db import db
from .models import Admin, Session, Parent, Child, Skill, Lesson, LessonHistory, Activity, ActivityHistory, Quiz, QuizHistory, Badge, BadgeHistory
from .demoData import createDummyData
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError
from datetime import datetime


def parent_regisc(request):
    # Function for parent registration that will later be sent as a request to the routes
    data=request.get_json()
    name=data.get('name')
    email=data.get('email_id')
    password=data.get('password')
    pic=data.get('profile_image')
    if pic == '':
        pic = None
    if None in (name,email,password):
        return jsonify({'error':'Invalid/Missing fields'}), 400
    else:
        parent=Parent.query.filter_by(email_id=email).first()
        if parent:
            return jsonify({'error':'Email already registered'}), 409

        hashed_password=generate_password_hash(password)
        new_parent=Parent(name=name,email_id=email,password=hashed_password,profile_image=pic)
        db.session.add(new_parent)
        db.session.commit()
        return jsonify({'message':'Parent Registered'}), 201

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
    if None in (name,username,password,dob):
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
        return jsonify({'message':'Child Registered'}), 201