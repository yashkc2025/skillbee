from io import BytesIO
from functools import wraps
import json
from pydoc import describe
from typing import List
from flask import request, jsonify, send_file
from .db import db
from .models import (
    Admin,
    Session,
    Parent,
    Child,
    Skill,
    Lesson,
    LessonHistory,
    Activity,
    ActivityHistory,
    Quiz,
    QuizHistory,
    Badge,
    BadgeHistory,
)
from .demoData import createDummyData
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date, timedelta
import uuid
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import and_, func, case, cast, Integer
import time
import base64
from .decorators import only_admin, only_admin_or_parent, only_parent

# import imghdr


def parent_regisc(request):
    # Function for parent registration that will later be sent as a request to the routes
    try:
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        pic = data.get("profile_image")
        if pic == "":
            pic = None
        if not all([name, email, password]):
            return jsonify({"error": "Invalid/Missing fields"}), 400
        else:
            parent = Parent.query.filter_by(email_id=email).first()
            if parent:
                return jsonify({"error": "Email already registered"}), 409
            if len(password) < 4:
                return (
                    jsonify(
                        {
                            "status": "error",
                            "message": "New password must be at least 4 characters long",
                        }
                    ),
                    400,
                )

            hashed_password = generate_password_hash(password)
            new_parent = Parent(
                name=name, email_id=email, password=hashed_password, profile_image=pic
            )
            db.session.add(new_parent)
            db.session.commit()
            session_id = str(uuid.uuid4())
            session_info = {
                "parent_id": new_parent.parent_id,
                "email": new_parent.email_id,
                "login_time": datetime.now().isoformat(),
            }
            new_session = Session(
                session_id=session_id, session_information=session_info
            )
            print(new_session)
            db.session.add(new_session)
            db.session.commit()
            return (
                jsonify(
                    {
                        "session": {
                            "token": session_id,
                            "login_time": session_info["login_time"],
                        },
                        "user": {"id": new_parent.parent_id},
                    }
                ),
                201,
            )
    except Exception as e:
        print(f"Parent registration error: {e}")
        return (
            jsonify({"error": "Something went wrong during parent registration"}),
            500,
        )


def age_calc(dob):
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))


def child_regisc(request):
    # Function for children registration that will later be sent as a request to the routes
    try:
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        username = data.get("username")
        password = data.get("password")
        dob_str = data.get("dob")
        school = data.get("school")
        pic = data.get("profile_image")
        if pic == "":
            pic = None
        if dob_str:
            try:
                dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
            except ValueError:
                return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
        else:
            dob = None
        if not all([name, username, password, dob]):
            return jsonify({"error": "Invalid/Missing fields"}), 400
        else:
            age = age_calc(dob)
            if age < 8 or age > 14:
                return (
                    jsonify({"error": "Only children aged 8 to 14 can register"}),
                    400,
                )
            else:
                children = Child.query.filter_by(username=username).first()
                if children:
                    return jsonify({"error": "Username already registered"}), 409
                if email and Child.query.filter_by(email_id=email).first():
                    return jsonify({"error": "Email already registered"}), 409
                if len(password) < 4:
                    return (
                        jsonify(
                            {
                                "status": "error",
                                "message": "New password must be at least 4 characters long",
                            }
                        ),
                        400,
                    )
                hashed_password = generate_password_hash(password)
                new_child = Child(
                    name=name,
                    email_id=email,
                    username=username,
                    password=hashed_password,
                    dob=dob,
                    school=school,
                    profile_image=pic,
                )
                db.session.add(new_child)
                db.session.commit()
                session_id = str(uuid.uuid4())
                session_info = {
                    "child_id": new_child.child_id,
                    "username": new_child.username,
                    "email": new_child.email_id if email else None,
                    "login_time": datetime.now().isoformat(),
                }
                new_session = Session(
                    session_id=session_id, session_information=session_info
                )

                db.session.add(new_session)
                db.session.commit()
                print(new_session)
                return (
                    jsonify(
                        {
                            "session": {
                                "token": session_id,
                                "login_time": session_info["login_time"],
                            },
                            "user": {"id": new_child.child_id},
                        }
                    ),
                    201,
                )
    except Exception as e:
        print(f"Registration error: {e}")
        return jsonify({"error": "Something went wrong during child registration"}), 500


def admin_create():
    # Function to create the admin automatically
    aemail = "admin@gmail.com"
    apassword = "1234"
    exist = Admin.query.filter_by(email_id=aemail).first()
    if not exist:
        hashedp = generate_password_hash(apassword)
        newa = Admin(email_id=aemail, password=hashedp)
        db.session.add(newa)
        db.session.commit()
        print("admin created")
    else:
        print("admin in database")


def admin_loginc():
    # Login function for the admin

    data = request.get_json()
    email = data.get("email_id")
    password = data.get("password")
    if not email or not password:
        return jsonify({"error": "Missing email or password"}), 500

    if len(password) < 4:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "New password must be at least 4 characters long",
                }
            ),
            400,
        )

    admin = Admin.query.filter_by(email_id=email).first()
    if not admin or not check_password_hash(admin.password, password):
        return jsonify({"error": "Invalid email or password"}), 401

    token = str(uuid.uuid4())
    session_info = {
        "admin_id": admin.admin_id,
        "email_id": admin.email_id,
        "login_time": datetime.now().isoformat(),
    }

    try:
        new_session = Session(session_id=token, session_information=session_info)
        db.session.add(new_session)
        db.session.commit()

        return (
            jsonify(
                {
                    "session": {
                        "token": token,
                        "login_time": session_info["login_time"],
                    },
                    "user": {"id": admin.admin_id},
                }
            ),
            200,
        )

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error occurred", "details": str(e)}), 500


def parent_loginc(request):
    """
    Handle parent login request by validating credentials and generating a session token.
    """
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    parent = Parent.query.filter_by(email_id=email).first()
    if not parent or not check_password_hash(parent.password, password):
        return jsonify({"error": "Invalid email or password"}), 401

    token = str(uuid.uuid4())
    session_info = {
        "parent_id": parent.parent_id,
        "email": parent.email_id,
        "login_time": datetime.now().isoformat(),
    }

    try:
        new_session = Session(session_id=token, session_information=session_info)
        db.session.add(new_session)
        db.session.commit()

        return (
            jsonify(
                {
                    "session": {
                        "token": token,
                        "login_time": session_info["login_time"],
                    },
                    "user": {"id": parent.parent_id},
                }
            ),
            200,
        )

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error occurred", "details": str(e)}), 500


def child_loginc(request):
    """
    Handle child login request by validating credentials and generating a session token.
    """
    data = request.get_json()
    identifier = data.get("username")
    password = data.get("password")

    if not identifier or not password:
        return jsonify({"error": "Missing required fields"}), 400

    child = Child.query.filter(
        (Child.username == identifier) | (Child.email_id == identifier)
    ).first()
    if not child or not check_password_hash(child.password, password):
        return jsonify({"error": "Invalid email or password"}), 401

    token = str(uuid.uuid4())
    session_info = {
        "child_id": child.child_id,
        "email": identifier,
        "login_time": datetime.now().isoformat(),
    }

    try:
        new_session = Session(session_id=token, session_information=session_info)
        db.session.add(new_session)
        db.session.commit()

        return (
            jsonify(
                {
                    "session": {
                        "token": token,
                        "login_time": session_info["login_time"],
                    },
                    "user": {"id": child.child_id},
                }
            ),
            200,
        )

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error occurred", "details": str(e)}), 500


# dashboard


def token_required(allowed_roles=None):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            if "Authorization" in request.headers:
                token = request.headers["Authorization"].split(" ")[-1]

            if not token:
                return jsonify({"error": "Token is missing"}), 401

            try:
                session = Session.query.filter_by(session_id=token).first()
                if not session:
                    return jsonify({"error": "Invalid token"}), 401

                session_info = session.session_information

                login_time = datetime.fromisoformat(session_info["login_time"])
                if datetime.now() > login_time + timedelta(hours=3):
                    db.session.delete(session)
                    db.session.commit()
                    return jsonify({"error": "Token has expired"}), 401

                current_user = None
                role = None

                if "admin_id" in session_info:
                    current_user = Admin.query.get(session_info["admin_id"])
                    role = "admin"
                elif "parent_id" in session_info:
                    current_user = Parent.query.get(session_info["parent_id"])
                    role = "parent"
                elif "child_id" in session_info:
                    current_user = Child.query.get(session_info["child_id"])
                    role = "child"

                if not current_user:
                    return jsonify({"error": "User not found"}), 401

                if allowed_roles and role not in allowed_roles:
                    return jsonify({"error": "Insufficient permissions"}), 403

                kwargs["current_user"] = current_user
                kwargs["role"] = role

                return f(*args, **kwargs)

            except SQLAlchemyError as e:
                db.session.rollback()
                return (
                    jsonify({"error": "Database error occurred", "details": str(e)}),
                    500,
                )

        return decorated

    return decorator


def get_auser(current_user, role):
    # this is according to auth.md and fetches the details of users from the session id as authorisation bearer BUT it returns full profile info
    if role == "child":
        return (
            jsonify(
                {
                    "user": {
                        "id": current_user.child_id,
                        "role": "child",
                        "username": current_user.username,
                        "email": current_user.email_id,
                        "dob": (
                            current_user.dob.isoformat() if current_user.dob else None
                        ),
                        "school": current_user.school,
                        "profile_image": None,
                        "name": current_user.name,
                    }
                }
            ),
            200,
        )
    elif role == "parent":
        return (
            jsonify(
                {
                    "user": {
                        "id": current_user.parent_id,
                        "role": "parent",
                        "name": current_user.name,
                        "email": current_user.email_id,
                        "profile_image": None,
                    }
                }
            ),
            200,
        )
    elif role == "admin":
        return (
            jsonify(
                {
                    "user": {
                        "id": current_user.admin_id,
                        "role": "admin",
                        "email": current_user.email_id,
                    }
                }
            ),
            200,
        )
    return jsonify({"error": "Invalid session data"}), 401


def get_child_dashboard_stats(child_id):
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
            LessonHistory.child_id == child_id, LessonHistory.lesson_id.in_(lesson_ids)
        ).count()
        if completed == len(lesson_ids):
            completed_skills += 1
    badges_earned = BadgeHistory.query.filter_by(child_id=child_id).count()
    child = Child.query.get(child_id)
    streak = child.streak if child else 0
    all_children = Child.query.order_by(Child.points.desc()).all()
    leaderboard_rank = next(
        (index + 1 for index, c in enumerate(all_children) if c.child_id == child_id),
        None,
    )
    
    return (
        jsonify(
            {
                "lessons_completed": lessons_completed,
                "skills_completed": completed_skills,
                "streak": streak,
                "badges_earned": badges_earned,
                "leaderboard_rank": leaderboard_rank
            }
        ),
        200,
    )

def get_child_heatmap(child_id):
    """
    Fetches all activity records for a child and returns them formatted
    for a heatmap.
    """
    try:
        date_counts = {}
        all_records = []
        all_records.extend(LessonHistory.query.filter_by(child_id=child_id).all())
        # all_records.extend(ActivityHistory.query.filter_by(child_id=child_id).all())
        all_records.extend(QuizHistory.query.filter_by(child_id=child_id).all())
        
        for record in all_records:
            date_str = record.created_at.strftime("%Y-%m-%d")

            if date_str in date_counts:
                date_counts[date_str] += 1
            else:
                date_counts[date_str] = 1

        heatmap = []
        for date, count in date_counts.items():
            heatmap.append({"date": date, "count": count})

        # --- FIX: Wrap the heatmap data in a dictionary.
        # The frontend expects a JSON object with a 'heatmap' key.
        return jsonify({"heatmap": heatmap}), 200

    except Exception as e:
        # It's good practice to log the error for debugging
        print(f"Error fetching child heatmap: {e}")
        return jsonify({"error": "Failed to fetch heatmap data"}), 500

def get_leaderboard(child_id):
    all_children = Child.query.filter_by(is_blocked=False).order_by(Child.points.desc()).all()

    leaderboard = []
    for index, child in enumerate(all_children, start=1):
        leaderboard.append({
            "rank": index,
            "id": child.child_id,
            "name": child.name,
            "username": child.username,
            "points": child.points,
            "streak": child.streak
        })

    return jsonify(leaderboard), 200

def get_user_skill_progress(child_id):
    # gets the child lesson progress
    child = Child.query.get(child_id)
    if not child:
        return jsonify({"error": "Child not found"}), 404
    
    age = age_calc(child.dob) # Assuming age_calc function is defined elsewhere
    
    # Get skills filtered by the child's age
    skills: List[Skill] = Skill.query.filter(
        Skill.min_age <= age, Skill.max_age > age
    ).all()
    
    response = []
    for skill in skills:
        total_lessons = Lesson.query.filter_by(skill_id=skill.skill_id).count()
        completed = (
            LessonHistory.query.join(Lesson)
            .filter(
                Lesson.skill_id == skill.skill_id, LessonHistory.child_id == child_id
            )
            .count()
        )
        percent = int((completed / total_lessons) * 100) if total_lessons else 0
        response.append(
            {
                "name": skill.name,
                "link": f"/skills/{skill.skill_id}",
                "percentage_completed": percent,
                "id": skill.skill_id,
            }
        )

    return jsonify(response), 200

def get_user_badges(child_id):
    # child_id = current_user.child_id

    # Get badge name and image by joining Badge and BadgeHistory
    data = (
        db.session.query(Badge.name, Badge.image)
        .join(BadgeHistory)
        .filter(BadgeHistory.child_id == child_id)
        .all()
    )

    # Convert image from binary to base64 string (for testing in JSON)
    response = []
    for name, image in data:
        image_str = base64.b64encode(image).decode("utf-8") if image else ""
        response.append({"name": name, "image": image_str})

    return jsonify(response), 200


def get_lesson_quizzes(child_id, lesson_id):
    lesson = Lesson.query.get(lesson_id)
    if not lesson:
        return jsonify({"error": "Lesson not found"}), 404
    curriculum = Skill.query.get(lesson.skill_id)
    if not curriculum:
        return jsonify({"error": "Curriculum not found"}), 404

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
            "time_duration": (
                f"{quiz.time_duration // 60} mins {quiz.time_duration % 60} sec" if quiz.time_duration else "no time limit"
            ),
            "difficulty": quiz.difficulty,
            "total_marks": len(quiz.questions),
            "no_questions": len(quiz.questions),
            "progress_status": 100 if quiz.quiz_id in attempted_quiz_ids else 0,
            "image": None,
        }
        quiz_list.append(quiz_data)
    return (
        jsonify(
            {
                "curriculum": {
                    "curriculum_id": curriculum.skill_id,
                    "name": curriculum.name,
                },
                "lesson": {"lesson_id": lesson.lesson_id, "title": lesson.title},
                "quizzes": quiz_list,
            }
        ),
        200,
    )


def get_curriculums_for_child(current_user, role, child_id):
    child = Child.query.get(child_id)
    if not child:
        return jsonify({"error": "Child not found"}), 404
    age = age_calc(child.dob)
    skills = Skill.query.filter(Skill.min_age <= age, Skill.max_age > age).all()
    skill_ids = [s.skill_id for s in skills]
    lessons = Lesson.query.filter(Lesson.skill_id.in_(skill_ids)).all()
    lesson_ids = [l.lesson_id for l in lessons]

    lesson_map = {}
    for lesson in lessons:
        lesson_map.setdefault(lesson.skill_id, []).append(lesson.lesson_id)
    activities = Activity.query.filter(Activity.lesson_id.in_(lesson_ids)).all()
    quizzes = Quiz.query.filter(Quiz.lesson_id.in_(lesson_ids)).all()
    completed_lessons = {
        lh.lesson_id
        for lh in LessonHistory.query.filter(
            LessonHistory.child_id == child_id, LessonHistory.lesson_id.in_(lesson_ids)
        )
    }
    completed_activities = {
        ah.activity_id
        for ah in ActivityHistory.query.filter(
            ActivityHistory.activity_id.in_([a.activity_id for a in activities])
        )
    }
    passed_quizzes = {
        qh.quiz_id
        for qh in QuizHistory.query.filter(
            QuizHistory.child_id == child_id,
            QuizHistory.quiz_id.in_([q.quiz_id for q in quizzes]),
            QuizHistory.score >= 40,
        )
    }
    result = []
    for skill in skills:
        lids = lesson_map.get(skill.skill_id, [])
        aids = [a.activity_id for a in activities if a.lesson_id in lids]
        qids = [q.quiz_id for q in quizzes if q.lesson_id in lids]
        total = len(lids) + len(aids) + len(qids)
        completed = (
            sum(1 for lid in lids if lid in completed_lessons)
            + sum(1 for aid in aids if aid in completed_activities)
            + sum(1 for qid in qids if qid in passed_quizzes)
        )
        progress = round((completed / total) * 100) if total else 0
        result.append(
            {
                "curriculum_id": skill.skill_id,
                "name": skill.name,
                "description": skill.description,
                "image": None,
                "progress_status": progress,
            }
        )

    return jsonify({"curriculums": result}), 200


def get_skill_lessons(child_id, skill_id):
    try:
        skill = Skill.query.get(skill_id)

        if not skill:
            return jsonify({"error": "Skill not found"}), 404

        lessons = (
            Lesson.query.filter_by(skill_id=skill_id).order_by(Lesson.position).all()
        )
        if not lessons:
            return []

        activities = Activity.query.filter(
            Activity.lesson_id.in_([lesson.lesson_id for lesson in lessons]),
            Activity.child_id == child_id,
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
                attempted_activities_by_lesson.setdefault(lesson_id, set()).add(
                    ah.activity_id
                )

        quizzes = Quiz.query.filter(
            Quiz.lesson_id.in_([lesson.lesson_id for lesson in lessons])
        ).all()

        quizzes_by_lesson = {}
        quiz_id_to_lesson_id = {}
        for quiz in quizzes:
            quizzes_by_lesson.setdefault(quiz.lesson_id, []).append(quiz)
            quiz_id_to_lesson_id[quiz.quiz_id] = quiz.lesson_id

        quiz_history = QuizHistory.query.filter(
            QuizHistory.quiz_id.in_(quiz_id_to_lesson_id.keys()),
            QuizHistory.child_id == child_id,
        ).all()

        attempted_quizzes_by_lesson = {}
        for qh in quiz_history:
            lesson_id = quiz_id_to_lesson_id.get(qh.quiz_id)
            if lesson_id:
                attempted_quizzes_by_lesson.setdefault(lesson_id, set()).add(qh.quiz_id)

        lessons_data = []
        for lesson in lessons:
            total_activities = len(activities_by_lesson.get(lesson.lesson_id, []))
            attempted_activities = len(
                attempted_activities_by_lesson.get(lesson.lesson_id, set())
            )
            total_quizzes = len(quizzes_by_lesson.get(lesson.lesson_id, []))
            attempted_quizzes = len(
                attempted_quizzes_by_lesson.get(lesson.lesson_id, set())
            )

            if lesson.image:
                image_base64 = base64.b64encode(lesson.image).decode("utf-8")
            else:
                image_base64 = ""

            lessons_data.append(
                {
                    "lesson_id": lesson.lesson_id,
                    "title": lesson.title,
                    "image": image_base64,
                    "description": lesson.description,
                    "progress_status": (
                        (
                            (attempted_quizzes + attempted_activities)
                            * 100
                            / (total_activities + total_quizzes)
                        )
                        if (total_activities + total_quizzes) > 0
                        else 100
                    ),
                }
            )

        return (
            jsonify(
                {
                    "curriculum": {
                        "curriculum_id": skill.skill_id,
                        "name": skill.name,
                    },
                    "lessons": lessons_data,
                }
            ),
            200,
        )
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error occurred", "details": str(e)}), 500


def get_lesson_details(child_id, lesson_id):
    try:
        lesson = Lesson.query.get(lesson_id)
        if not lesson:
            return jsonify({"error": "Lesson not found"}), 404

        lesson_history = LessonHistory.query.filter_by(
            child_id=child_id, lesson_id=lesson_id
        ).first()

        lesson_data = {
            "lesson_id": lesson.lesson_id,
            "title": lesson.title,
            "content": lesson.content,
            "image": lesson.image,
            "completed_at": (
                lesson_history.created_at.isoformat() if lesson_history else None
            ),
        }

        return jsonify(lesson_data), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error occurred", "details": str(e)}), 500


def mark_lesson_completed(child_id, lesson_id, completed_at=None):
    try:
        lesson = Lesson.query.get(lesson_id)
        if not lesson:
            return jsonify({"error": "Lesson not found"}), 404

        existing_history = LessonHistory.query.filter_by(
            child_id=child_id, lesson_id=lesson_id
        ).first()

        if existing_history:
            return jsonify({"message": "Lesson already completed"}), 200

        # Convert completed_at string to datetime object if provided
        if completed_at:
            if isinstance(completed_at, str):
                try:
                    # Handle ISO format with 'Z' suffix
                    if completed_at.endswith("Z"):
                        completed_at = completed_at[:-1] + "+00:00"
                    completed_at = datetime.fromisoformat(completed_at)
                except ValueError:
                    return jsonify({"error": "Invalid date format"}), 400
        else:
            completed_at = datetime.now()

        new_history = LessonHistory(
            child_id=child_id, lesson_id=lesson_id, created_at=completed_at
        )

        db.session.add(new_history)
        db.session.commit()

        return jsonify({"message": "Lesson marked as completed"}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error occurred", "details": str(e)}), 500


def get_lesson_activities(child_id, lesson_id):
    try:
        lesson = Lesson.query.get(lesson_id)
        if not lesson:
            return []

        skill = Skill.query.get(lesson.skill_id)
        if not skill:
            return jsonify({"error": "Curriculum not found"}), 404

        activities = Activity.query.filter_by(lesson_id=lesson_id).all()

        activity_submissions = ActivityHistory.query.filter(
            ActivityHistory.activity_id.in_([a.activity_id for a in activities])
        ).all()

        completed_activities = {
            submission.activity_id for submission in activity_submissions
        }

        activities_data = []
        for activity in activities:
            if activity.image:
                image_base64 = base64.b64encode(activity.image).decode("utf-8")
            else:
                image_base64 = ""

            activities_data.append(
                {
                    "activity_id": activity.activity_id,
                    "name": activity.name,
                    "description": activity.description,
                    "image": image_base64,
                    "progress_status": (
                        100 if activity.activity_id in completed_activities else 0
                    ),
                }
            )

        response_data = {
            "curriculum": {"curriculum_id": skill.skill_id, "name": skill.name},
            "lesson": {"lesson_id": lesson.lesson_id, "title": lesson.title},
            "activities": activities_data,
        }

        return jsonify(response_data), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error occurred", "details": str(e)}), 500


def get_activity_details(child_id, activity_id):
    try:
        activity = Activity.query.filter_by(
            activity_id=activity_id, child_id=child_id
        ).first()

        if not activity:
            return jsonify({"error": "Activity not found"}), 404

        activity_history = (
            ActivityHistory.query.filter_by(activity_id=activity_id)
            .order_by(ActivityHistory.created_at.desc())
            .first()
        )

        activity_data = {
            "activity_id": activity.activity_id,
            "name": activity.name,
            "description": activity.description,
            "image": activity.image,
            "answer_format": activity.answer_format,
            "completed_at": (
                activity_history.created_at.isoformat() if activity_history else None
            ),
        }
        return jsonify(activity_data), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error occurred", "details": str(e)}), 500


def submit_activity(child_id, activity_id):
    try:
        activity = Activity.query.filter_by(
            activity_id=activity_id, child_id=child_id
        ).first()
        if not activity:
            return jsonify({"error": "Activity not found"}), 404

        file_data = None
        file_extension = None

        # Handle multipart/form-data uploads
        if request.files and "file" in request.files:
            uploaded_file = request.files["file"]

            if uploaded_file.filename == "":
                return jsonify({"error": "No file selected"}), 400

            file_extension = uploaded_file.filename.lower().split(".")[-1]
            file_data = uploaded_file.read()

        # Handle raw binary uploads (Content-Type: image/jpeg, etc.)
        elif request.content_type and request.content_type.startswith(
            ("image/", "application/pdf")
        ):
            file_data = request.get_data()

            # Determine extension from content type
            content_type_map = {
                "image/jpeg": "jpg",
                "image/jpg": "jpg",
                "image/png": "png",
                "application/pdf": "pdf",
            }
            file_extension = content_type_map.get(request.content_type, "jpg")

        else:
            return (
                jsonify({"error": "No file uploaded or unsupported content type"}),
                400,
            )

        if not file_data:
            return jsonify({"error": "No file data received"}), 400

        # Check file size (10MB limit)
        max_file_size = 10 * 1024 * 1024  # 10MB in bytes
        if len(file_data) > max_file_size:
            return (
                jsonify({"error": "File size too large. Maximum allowed size is 10MB"}),
                400,
            )

        # Validate file format
        allowed_extensions = ["jpg", "jpeg", "png", "pdf"]
        if file_extension not in allowed_extensions:
            return (
                jsonify(
                    {
                        "error": "Invalid file format. Only JPG, JPEG, PNG, or PDF allowed"
                    }
                ),
                400,
            )

        submission_time = datetime.now()

        activity_submission = ActivityHistory(
            activity_id=activity_id, answer=file_data, created_at=submission_time
        )

        db.session.add(activity_submission)
        db.session.commit()

        return (
            jsonify(
                {
                    "activity_history_id": activity_submission.activity_history_id,
                    "submitted_at": submission_time.isoformat(),
                }
            ),
            201,
        )

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error occurred", "details": str(e)}), 500


def get_activity_history(child_id, activity_id):
    try:
        activity = Activity.query.filter_by(
            activity_id=activity_id, child_id=child_id
        ).first()
        if not activity:
            return jsonify({"error": "Activity not found"}), 404

        submissions = (
            ActivityHistory.query.filter_by(activity_id=activity_id)
            .order_by(ActivityHistory.created_at.desc())
            .all()
        )

        activities_submission = []
        for submission in submissions:
            submission_data = {
                "activity_history_id": submission.activity_history_id,
                "activity_id": submission.activity_id,
                "submitted_at": submission.created_at.isoformat(),
                "feedback": submission.feedback if submission.feedback else None,
            }
            activities_submission.append(submission_data)

        return jsonify({"activities_submission": activities_submission}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error occurred", "details": str(e)}), 500


def get_activity_submission(child_id, activity_history_id):
    try:
        submission = ActivityHistory.query.get(activity_history_id)
        if not submission:
            return jsonify({"error": "Submission not found"}), 404

        activity = Activity.query.filter_by(
            activity_id=submission.activity_id, child_id=child_id
        ).first()

        if not activity:
            return jsonify({"error": "Associated activity not found"}), 404

        if not submission.answer:
            return jsonify({"error": "No file found for this submission"}), 404

        # Detect file type from binary data
        file_data = submission.answer

        # Check file signatures (magic numbers) to determine actual file type
        if file_data.startswith(b"\xff\xd8\xff"):  # JPEG
            content_type = "image/jpeg"
            file_extension = "jpg"
        elif file_data.startswith(b"\x89PNG\r\n\x1a\n"):  # PNG
            content_type = "image/png"
            file_extension = "png"
        elif file_data.startswith(b"%PDF"):  # PDF
            content_type = "application/pdf"
            file_extension = "pdf"
        else:
            # Fallback to activity.answer_format if available
            if activity.answer_format and activity.answer_format.lower() == "pdf":
                content_type = "application/pdf"
                file_extension = "pdf"
            elif activity.answer_format and activity.answer_format.lower() == "image":
                content_type = "image/jpeg"  # Default to JPEG for images
                file_extension = "jpg"
            else:
                content_type = "application/octet-stream"
                file_extension = "bin"

        return send_file(
            BytesIO(submission.answer),
            mimetype=content_type,
            as_attachment=True,
            download_name=f"submission_{activity_history_id}.{file_extension}",
        )

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error occurred", "details": str(e)}), 500


# def get_lesson_quizzes(child_id, lesson_id):
#     try:
#         lesson = Lesson.query.filter_by(lesson_id=lesson_id).first()
#         if not lesson:
#             return (
#                 jsonify(
#                     {"error": "Lesson not found or does not belong to the curriculum"}
#                 ),
#                 404,
#             )

#         skill = Skill.query.filter_by(skill_id=lesson.skill_id).first()
#         if not skill:
#             return jsonify({"error": "Curriculum not found"}), 404

#         quizzes = Quiz.query.filter_by(lesson_id=lesson_id).all()

#         quiz_history = QuizHistory.query.filter(
#             QuizHistory.quiz_id.in_([quiz.quiz_id for quiz in quizzes]),
#             QuizHistory.child_id == child_id,
#         ).all()

#         attempted_quizzes = {history.quiz_id for history in quiz_history}

#         quizzes_data = []
#         for quiz in quizzes:
#             quizzes_data.append(
#                 {
#                     "quiz_id": quiz.quiz_id,
#                     "name": quiz.quiz_name,
#                     "description": quiz.description,
#                     "time_duration": quiz.time_duration,
#                     "progress_status": 100 if quiz.quiz_id in attempted_quizzes else 0,
#                     "image": quiz.image,
#                 }
#             )

#         response_data = {
#             "curriculum": {"curriculum_id": skill.skill_id, "name": skill.name},
#             "lesson": {"lesson_id": lesson.lesson_id, "title": lesson.title},
#             "quizzes": quizzes_data,
#         }

#         return jsonify(response_data), 200

#     except SQLAlchemyError as e:
#         db.session.rollback()
#         return jsonify({"error": "Database error occurred", "details": str(e)}), 500


# @token_required(allowed_roles=["child"])
def get_quiz_history(current_user, role, quiz_id):
    # Get teh quiz history
    child_id = current_user.child_id
    histories = QuizHistory.query.filter_by(child_id=child_id, quiz_id=quiz_id).all()
    if not histories:
        return jsonify({"quizzes_history": []}), 200
    child = Child.query.get(child_id)
    parent_name = child.parent.name if child.parent else None
    parent_email = child.parent.email_id if child.parent else None
    history_list = []
    for h in histories:
        history_list.append(
            {
                "quiz_history_id": h.quiz_history_id,
                "quiz_id": h.quiz_id,
                "attempted_at": (
                    h.created_at.isoformat() if hasattr(h, "created_at") else "N/A"
                ),
                "score": h.score,
                "feedback": {
                    "admin": "admin@gmail.com",
                    "parent": (
                        f"Parent: {parent_name} ({parent_email})" if parent_name else ""
                    ),
                },
            }
        )
    return jsonify({"quizzes_history": history_list}), 200


def get_quiz_history(child_id, quiz_id):
    try:
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return jsonify({"error": "Quiz not found"}), 404

        quiz_attempts = (
            QuizHistory.query.filter_by(child_id=child_id, quiz_id=quiz_id)
            .order_by(QuizHistory.created_at.desc())
            .all()
        )

        quizzes_history = []
        for attempt in quiz_attempts:
            quizzes_history.append(
                {
                    "quiz_history_id": attempt.quiz_history_id,
                    "quiz_id": attempt.quiz_id,
                    "attempted_at": attempt.created_at.isoformat(),
                    "score": attempt.score,
                    "feedback": attempt.feedback if attempt.feedback else None,
                }
            )

        return jsonify({"quizzes_history": quizzes_history}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error occurred", "details": str(e)}), 500


def get_quiz_questions(curriculum_id, lesson_id, quiz_id):

    try:
        # Validate curriculum exists
        curriculum = Skill.query.get(curriculum_id)
        if not curriculum:
            return jsonify({"error": "Curriculum not found"}), 404

        # Validate lesson exists and belongs to curriculum
        lesson = Lesson.query.filter_by(
            lesson_id=lesson_id, skill_id=curriculum_id
        ).first()
        if not lesson:
            return (
                jsonify(
                    {"error": "Lesson not found or does not belong to the curriculum"}
                ),
                404,
            )

        # Validate quiz exists and belongs to lesson
        quiz = Quiz.query.filter_by(quiz_id=quiz_id, lesson_id=lesson_id).first()
        if not quiz:
            return (
                jsonify({"error": "Quiz not found or does not belong to the lesson"}),
                404,
            )

        # Format questions with index
        questions_data = []
        if quiz.questions:  # questions is stored as JSON
            for idx, question in enumerate(quiz.questions):
                question_data = {
                    "question_index": idx + 1,
                    "question": question.get("question", ""),
                    "options": question.get("options", []),
                    "marks": question.get("marks", 1),
                }
                questions_data.append(question_data)

        response_data = {
            "curriculum": {
                "curriculum_id": curriculum.skill_id,
                "name": curriculum.name,
            },
            "lesson": {"lesson_id": lesson.lesson_id, "title": lesson.title},
            "quizzes": {
                "quiz_id": quiz.quiz_id,
                "name": quiz.quiz_name,
                "time_duration": quiz.time_duration,
            },
            "questions": questions_data,
        }

        return jsonify(response_data), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error occurred", "details": str(e)}), 500


def submit_quiz(child_id, quiz_id):
    """
    Submit quiz answers and calculate score.
    Frontend sends a dictionary of { "0-based-q-index": "0-based-o-index" }
    """
    try:

        # Validate quiz exists
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return jsonify({"error": "Quiz not found"}), 404

        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        answers = data.get("answers")
        # if not answers or not isinstance(answers, dict):
        #     return (
        #         jsonify(
        #             {
        #                 "error": "Invalid answers format. Expected dictionary with question_index: option_index"
        #             }
        #         ),
        #         400,
        #     )

        # Validate quiz has questions and answers
        if not quiz.questions or not quiz.answers:
            return jsonify({"error": "Quiz has no questions or answer key"}), 500

        # Validate questions and answers arrays have same length
        if len(quiz.questions) != len(quiz.answers):
            return (
                jsonify(
                    {
                        "error": "Quiz data inconsistency: questions and answers count mismatch"
                    }
                ),
                500,
            )

        score = 0
        total_questions = len(quiz.questions)
        total_score = sum(q.get("marks", 1) for q in quiz.questions)

        option_index = question_index = len(answers)
        # Process each submitted answer
        for q_idx_str, submitted_o_idx_str in answers.items():
            try:
                # Convert string indices to integers
                q_idx = int(q_idx_str)
                submitted_o_idx = int(submitted_o_idx_str)
            except (ValueError, TypeError):
                continue

            # Validate question index (1-based indexing)
            if question_index < 1 or question_index > total_questions:
                continue

            array_index = question_index - 1

            question_data = quiz.questions[array_index]
            answer_data = quiz.answers[array_index]

            options = question_data.get("options", [])
            question_marks = question_data.get("marks", 1)
            correct_answer = answer_data.get("correct_answer", "")

            # Validate option index (0-based indexing)
            if option_index < 0 or option_index >= len(options):
                continue  # Skip invalid option index

            # Get selected option
            selected_option = options[option_index]

            # Extract option text (handle both string and dict formats)
            if isinstance(selected_option, dict):
                selected_option_text = selected_option.get("text", "")
            elif isinstance(selected_option, str):
                selected_option_text = selected_option
            else:
                selected_option_text = str(selected_option)

            # Check if selected option is correct (single correct answer)
            if selected_option_text == correct_answer:
                score += question_marks
        # Save quiz attempt to history
        print([child_id, quiz_id, score])
        quiz_history = QuizHistory(
            child_id=child_id,
            quiz_id=quiz_id,
            score=score,
            created_at=datetime.now(),
            responses=answers,
        )
        db.session.add(quiz_history)
        db.session.commit()

        return jsonify({"score": score, "total_score": total_score}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error occurred", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    

def get_child_quiz_history(curriculum_id, lesson_id, quiz_id, quiz_history_id):
    try:
        # Validate quiz history exists
        quiz_history = QuizHistory.query.get(quiz_history_id)
        if not quiz_history:
            return jsonify({"error": "Quiz history not found"}), 404
        # Validate quiz exists
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return jsonify({"error": "Quiz not found"}), 404
        # Validate curriculum exists
        curriculum = Skill.query.get(curriculum_id)
        if not curriculum:
            return jsonify({"error": "Curriculum not found"}), 404
        # Validate lesson exists and belongs to curriculum
        lesson = Lesson.query.filter_by(
            lesson_id=lesson_id, skill_id=curriculum_id
        ).first()
        if not lesson:
            return (
                jsonify(
                    {"error": "Lesson not found or does not belong to the curriculum"}
                ),
                404,
            )
        # Format questions with index
        questions_data = []
        if quiz.questions:  # questions is stored as JSON
            for idx, question in enumerate(quiz.questions):
                question_data = {
                    "question_index": idx + 1,
                    "question": question.get("question", ""),
                    "options": question.get("options", []),
                    "marks": question.get("marks", 1),
                }
                questions_data.append(question_data)
        # Prepare response data
        response_data = {
            "curriculum": {
                "curriculum_id": curriculum.skill_id,
                "name": curriculum.name,
            },
            "lesson": {"lesson_id": lesson.lesson_id, "title": lesson.title},
            "quizzes": {
                "quiz_id": quiz.quiz_id,
                "name": quiz.quiz_name,
                "time_duration": quiz.time_duration,
            },
            "questions": questions_data,
            "quiz_history": {
                "quiz_history_id": quiz_history.quiz_history_id,
                "child_id": quiz_history.child_id,
                "quiz_id": quiz_history.quiz_id,
                "score": quiz_history.score,
                "created_at": quiz_history.created_at.isoformat(),
                "responses": quiz_history.responses,
            },
        }
        return jsonify(response_data), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error occurred", "details": str(e)}), 500


def get_child_profile_controller(child_id):
    try:
        child = Child.query.get(child_id)
        if not child:
            return jsonify({"error": "Child not found"}), 404

        profile_data = {
            "profile_image_url": child.profile_image if child.profile_image else "",
            "name": child.name,
            "dob": child.dob.isoformat() if child.dob else None,
            "email": child.email_id,
            "school": child.school,
        }

        return jsonify(profile_data), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error occurred", "details": str(e)}), 500


def update_child_profile(child_id):
    try:
        child = Child.query.get(child_id)
        if not child:
            return jsonify({"error": "Child not found"}), 404

        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Check if at least one field is provided
        allowed_fields = ["name", "email", "dob", "school"]
        if not any(field in data for field in allowed_fields):
            return jsonify({"error": "At least one field must be provided"}), 400

        # Update name if provided
        if "name" in data:
            if not data["name"] or not data["name"].strip():
                return jsonify({"error": "Name cannot be empty"}), 400
            child.name = data["name"].strip()

        # Update email if provided
        if "email" in data:
            email = data["email"]
            if email:  # If email is not empty, validate it
                # Check if email is already taken by another child
                existing_child = Child.query.filter(
                    Child.email_id == email, Child.child_id != child_id
                ).first()
                if existing_child:
                    return (
                        jsonify({"error": "Email already registered by another child"}),
                        409,
                    )
                child.email_id = email
            else:
                child.email_id = None  # Allow setting email to null

        # Update date of birth if provided
        if "dob" in data:
            dob_str = data["dob"]
            if dob_str:
                try:
                    dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
                    # Validate age (8-14 years old)
                    age = age_calc(dob)
                    if age < 8 or age > 14:
                        return (
                            jsonify(
                                {"error": "Child must be between 8 and 14 years old"}
                            ),
                            400,
                        )
                    child.dob = dob
                except ValueError:
                    return (
                        jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}),
                        400,
                    )
            else:
                return jsonify({"error": "Date of birth cannot be empty"}), 400

        # Update school if provided
        if "school" in data:
            child.school = data["school"]  # Allow school to be empty/null

        db.session.commit()

        return jsonify({"status": "success", "message": "Profile details updated"}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error occurred", "details": str(e)}), 500


def change_child_password(child_id):
    try:
        child = Child.query.get(child_id)
        if not child:
            return jsonify({"status": "error", "message": "Child not found"}), 404

        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No data provided"}), 400

        current_password = data.get("current_password")
        new_password = data.get("new_password")
        confirm_password = data.get("confirm_password")

        # Validate required fields
        if not all([current_password, new_password, confirm_password]):
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "Current password, new password, and confirm password are required",
                    }
                ),
                400,
            )

        # Verify current password
        if not check_password_hash(child.password, current_password):
            return (
                jsonify(
                    {"status": "error", "message": "Current password is incorrect"}
                ),
                400,
            )

        # Validate new password matches confirm password
        if new_password != confirm_password:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "New password and confirm password do not match",
                    }
                ),
                400,
            )

        # Validate new password length (optional - add your own requirements)
        if len(new_password) < 4:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "New password must be at least 4 characters long",
                    }
                ),
                400,
            )

        # Ensure new password is different from current password
        if check_password_hash(child.password, new_password):
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "New password must be different from current password",
                    }
                ),
                400,
            )

        # Hash and update the new password
        child.password = generate_password_hash(new_password)
        db.session.commit()

        return (
            jsonify({"status": "success", "message": "Password changed successfully"}),
            200,
        )

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": "Database error occurred"}), 500


import base64


def child_profile_image(child_id):
    """
    Handle both GET and POST requests for child profile images.
    GET: Retrieves profile image as a Base64 Data URL.
    POST: Uploads/updates profile image from a Base64 Data URL.
    """
    try:
        child = Child.query.get(child_id)

        if request.method == "POST":
            data = request.get_json()
            pic = (
                data.get("profile_image") if (data.get("profile_image") != "") else None
            )

            child.profile_image = pic
            db.session.commit()
            return (
                jsonify({"status": "success", "message": "Profile image updated"}),
                200,
            )

        elif request.method == "GET":
            return (
                jsonify(
                    {
                        "profile_image": (
                            child.profile_image if child.profile_image else ""
                        ),
                    }
                ),
                200,
            )

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": "Database error occurred"}), 500

def get_child_badges(child_id):
    """Retrieve all badges earned by a child.
    """
    try:
        child = Child.query.get(child_id)
        if not child:
            return jsonify({"error": "Child not found"}), 404
        badges = Badge.query.join(BadgeHistory).filter(BadgeHistory.child_id == child_id).all()
        response = []
        for badge in badges:
            if badge.image:
                image_base64 = base64.b64encode(badge.image).decode("utf-8")
            else:
                image_base64 = ""
            response.append(
                {
                    "id": badge.badge_id,
                    "label": badge.name,
                    "image": image_base64
                }
            )
        return jsonify(response), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error occurred", "details": str(e)}), 500

def get_children(current_user, role):
    # Admin: all children; Parent: only their children
    if role == "admin":
        children = Child.query.all()
    elif role == "parent":
        children = Child.query.filter_by(parent_id=current_user.parent_id).all()
    else:
        return jsonify({"error": "Forbidden"}), 403

    response = []
    for child in children:
        if child.profile_image:
            image_base64 = base64.b64encode(child.profile_image).decode("utf-8")
        else:
            image_base64 = ""

        response.append(
            {
                "id": child.child_id,
                "image": image_base64,
                "name": child.name,
                "email": child.email_id,
                "age": age_calc(child.dob),
                "school_name": child.school,
                "last_login": (
                    child.last_login.isoformat() if child.last_login else None
                ),
            }
        )

    return jsonify(response), 200


def get_lessons(current_user, role):
    lessons = Lesson.query.all()
    response = []
    for lesson in lessons:
        # curriculum is the associated Skill name
        response.append(
            {
                "id": lesson.lesson_id,
                "title": lesson.title,
                "curriculum": lesson.skill.name if lesson.skill else None,
            }
        )
    return jsonify(response), 200


def get_quizzes(current_user, role):
    lesson_id = request.args.get("lesson_id", type=int)

    query = Quiz.query
    if lesson_id is not None:
        query = query.filter_by(lesson_id=lesson_id)

    quizzes = query.all()
    result = []
    for quiz in quizzes:
        lesson = quiz.lesson
        skill = lesson.skill if lesson else None
        result.append(
            {
                "id": quiz.quiz_id,
                "title": quiz.quiz_name,
                "lesson": lesson.title if lesson else None,
                "curriculum": skill.name if skill else None,
            }
        )

    return jsonify(result)


def get_activities(current_user, role):
    lesson_id = request.args.get("lesson_id", type=int)

    query = Activity.query
    if lesson_id is not None:
        query = query.filter_by(lesson_id=lesson_id)

    activities = query.all()

    response = []
    for activity in activities:
        lesson = activity.lesson
        skill = lesson.skill if lesson else None

        response.append(
            {
                "id": activity.activity_id,
                "title": activity.name,
                "lesson": lesson.title if lesson else None,
                "curriculum": skill.name if skill else None,
            }
        )

    return jsonify(response)


def get_badges(current_user, role):
    badges = Badge.query.all()
    response = []

    for badge in badges:
        # Convert binary image to base64 string (if available)
        if badge.image:
            image_base64 = base64.b64encode(badge.image).decode("utf-8")
        else:
            image_base64 = ""

        response.append(
            {
                "id": badge.badge_id,
                "label": badge.name,
                "image": image_base64,
                "points": badge.points,
            }
        )

    return jsonify(response), 200


def create_child(current_user, role):
    data = request.get_json()

    # Required fields as per contract
    required_fields = ["name", "username", "password", "confirmPass", "dob", "school"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    name = data["name"].strip()
    username = data["username"].strip()
    password = data["password"]
    confirm_password = data["confirmPass"]
    dob_str = data["dob"].strip()
    school = data["school"].strip()

    # Image is optional; if present, decode base64
    pic = data.get("profile_image")
    if pic and pic != "":
        try:
            profile_image = base64.b64decode(pic)
        except Exception:
            return jsonify({"error": "Invalid base64 image for profile_image"}), 400
    else:
        profile_image = None

    # Password confirmation and length checks
    if password != confirm_password:
        return jsonify({"error": "Password and confirm password do not match"}), 400
    if len(password) < 4:
        return jsonify({"error": "Password must be at least 4 characters long"}), 400

    # Date and age validation
    try:
        dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Invalid DOB format. Expected YYYY-MM-DD."}), 400

    age = age_calc(dob)
    if age < 8 or age > 14:
        return jsonify({"error": "Only children aged 8 to 14 can register"}), 400

    # Uniqueness checks
    if Child.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 409

    # Optionally check for email if your form allows (some models have nullable email)
    email = data.get("email")
    if email and Child.query.filter_by(email_id=email).first():
        return jsonify({"error": "Email already registered"}), 409

    hashed_password = generate_password_hash(password)

    new_child = Child(
        name=name,
        username=username,
        password=hashed_password,
        dob=dob,
        school=school,
        parent_id=current_user.parent_id,  # comes directly from token/session
        profile_image=profile_image,
        email_id=email if email else None,
    )

    db.session.add(new_child)
    db.session.commit()

    return (
        jsonify(
            {
                "id": new_child.child_id,
                "name": new_child.name,
                "username": new_child.username,
                "dob": new_child.dob.isoformat(),
                "school": new_child.school,
            }
        ),
        201,
    )


def get_parents(current_user, role):
    parents = Parent.query.all()

    response = []
    for parent in parents:
        response.append(
            {
                "id": parent.parent_id,
                "name": parent.name,
                "email": parent.email_id,
                "blocked": parent.is_blocked,
            }
        )

    return jsonify(response), 200


def create_badge(current_user, role):
    data = request.get_json()
    name = data.get("title")
    description = data.get("description", "")
    image = data.get("image")
    points = data.get("points")

    if not name or not points or not description:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        if image:
            image_binary = base64.b64decode(image)
        else:
            image_binary = None
    except Exception:
        return jsonify({"error": "Invalid base64 image"}), 400

    badge = Badge(name=name, description=description, image=image_binary, points=points)

    db.session.add(badge)
    db.session.commit()

    return jsonify({"message": "Badge Created"}, 201)


def create_activity(current_user, role):
    data = request.get_json()
    required_fields = [
        "title",
        "description",
        "image",
        "instructions",
        "difficulty",
        "answer_format",
        "lesson_id",
    ]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    title = data["title"]
    description = data["description"]
    image = data["image"]
    instructions = data["instructions"]
    difficulty = data["difficulty"]
    answer_format = data["answer_format"]
    lesson_id = data["lesson_id"]

    try:
        if image:
            image_base64 = base64.b64decode(image)
        else:
            image_base64 = None
    except Exception:
        return jsonify({"error": "Invalid base64 image"}), 400
    allowed_formats = ["text", "image", "pdf"]
    if answer_format not in allowed_formats:
        return (
            jsonify(
                {"error": "Invalid answer_format. Must be one of: text, image, pdf"}
            ),
            400,
        )

    activity = Activity(
        name=title,
        description=description,
        instructions=instructions,
        difficulty=difficulty,
        image=image_base64,
        lesson_id=lesson_id,
        answer_format=answer_format,
    )
    db.session.add(activity)
    db.session.commit()

    return (
        jsonify(
            {
                "id": activity.activity_id,
                "title": activity.name,
                "answer_format": activity.answer_format,
                "difficulty": activity.difficulty,
            }
        ),
        201,
    )


def create_skills():
    skills = [
        {
            "name": "Critical Thinking",
            "description": "Improve Critical Thinking",
            "min_age": 8,
            "max_age": 14,
        },
        {
            "name": "Communication Skills",
            "description": "Improve communication.",
            "min_age": 8,
            "max_age": 14,
        },
        {
            "name": "Time Management",
            "description": "Learn to manage Time",
            "min_age": 8,
            "max_age": 14,
        },
        {
            "name": "Extracurricular Activities",
            "description": "Extra Activities",
            "min_age": 8,
            "max_age": 14,
        },
        {
            "name": "Financial Literacy",
            "description": "Understand Money",
            "min_age": 8,
            "max_age": 14,
        },
    ]

    for skill in skills:
        existing = Skill.query.filter_by(name=skill["name"]).first()
        if not existing:
            skill = Skill(
                name=skill["name"],
                description=skill["description"],
                min_age=skill["min_age"],
                max_age=skill["max_age"],
                image=None,
            )
            db.session.add(skill)
    db.session.commit()


def create_lesson(current_user, role):
    try:
        data = request.get_json()
        print("Received data:", data)
    except Exception as e:
        print("Error parsing JSON:", e)
        return jsonify({"error": "Invalid JSON"}), 400

    required = ["title", "content", "image", "skill_id"]
    if not all(k in data for k in required):
        return jsonify({"error": "Missing required fields"}), 400

    skill_id = data["skill_id"]
    title = data["title"]
    content_raw = data["content"]
    image_base64 = data["image"]
    description = data.get("description", None)

    skill = Skill.query.get(skill_id)
    if not skill:
        return jsonify({"error": "Invalid curriculum_id"}), 404

    try:
        # content = json.loads(content_raw) if isinstance(content_raw, str) else content_raw
        content = content_raw
    except json.JSONDecodeError:
        return jsonify({"error": "Content must be valid JSON"}), 400

    try:
        image_binary = base64.b64decode(image_base64) if image_base64 else None
    except Exception as e:
        print("Image decoding error:", e)
        return jsonify({"error": "Invalid base64 image"}), 400

    try:
        max_position = (
            db.session.query(db.func.max(Lesson.position))
            .filter_by(skill_id=skill_id)
            .scalar()
        )
        next_position = (max_position or 0) + 1

        lesson = Lesson(
            skill_id=skill_id,
            title=title,
            content=content,
            description=description,
            image=image_binary,
            position=next_position,
        )

        db.session.add(lesson)
        db.session.commit()

        return (
            jsonify(
                {
                    "id": lesson.lesson_id,
                    "title": lesson.title,
                    "curriculum": skill.name,
                    "position": lesson.position,
                }
            ),
            201,
        )
    except Exception as e:
        print("DB Error:", e)
        db.session.rollback()
        return jsonify({"error": "Database error"}), 500


def create_quiz(current_user, role):
    try:
        data = request.get_json()
    except Exception:
        return jsonify({"error": "Invalid JSON format"}), 400
    required_fields = [
        "title",
        "image",
        "description",
        "difficulty",
        "time_duration",
        "points",
        "questions",
        "lesson_id",
    ]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    lesson_id = data.get("lesson_id")

    lesson = Lesson.query.get(lesson_id)
    if not lesson:
        return jsonify({"error": "Lesson not found"}), 404
    title = data["title"]
    picture = data["image"]
    description = data["description"]
    difficulty = data["difficulty"]
    points = data["points"]
    time_duration = data["time_duration"]
    questions = data["questions"]

    try:
        image_binary = base64.b64decode(picture) if picture else None
    except Exception:
        return jsonify({"error": "Invalid base64 image"}), 400

    if not isinstance(questions, list) or not questions:
        return jsonify({"error": "questions must be a non-empty list"}), 400

    questions_json = []
    answers_json = []

    for idx, question in enumerate(questions):
        q_text = question.get("question")
        opts = question.get("options", [])

        if not q_text or not isinstance(opts, list) or not opts:
            return jsonify({"error": f"Invalid format in question #{idx + 1}"}), 400

        questions_json.append({"question": q_text, "options": opts})

        correct_answers = [opt["text"] for opt in opts if opt.get("isCorrect") is True]
        if not correct_answers:
            return (
                jsonify(
                    {"error": f"No correct answer specified for question '{q_text}'"}
                ),
                400,
            )

        answers_json.append({"question": q_text, "correct_answers": correct_answers})

    max_position = (
        db.session.query(db.func.max(Quiz.position))
        .filter_by(lesson_id=lesson_id)
        .scalar()
    )
    next_position = (max_position or 0) + 1

    quiz = Quiz(
        quiz_name=title,
        description=description,
        questions=questions_json,
        answers=answers_json,
        difficulty=difficulty,
        points=points,
        image=image_binary,
        lesson_id=lesson_id,
        position=next_position,
        is_visible=True,
        created_at=datetime.now(),
        time_duration=time_duration,
    )

    db.session.add(quiz)
    db.session.commit()

    return (
        jsonify(
            {
                "id": quiz.quiz_id,
                "title": quiz.quiz_name,
                "difficulty": quiz.difficulty,
                "points": quiz.points,
            }
        ),
        201,
    )


def admin_child_profile(current_user, role):
    child_id = request.args.get("id", type=int)
    if not child_id:
        return jsonify({"error": "Child ID is required as query param id="}), 400

    child = Child.query.get(child_id)
    if not child:
        return jsonify({"error": "Child not found"}), 404

    # Ensure parent can only access their own child
    if role == "parent" and child.parent_id != current_user.parent_id:
        return jsonify({"error": "Access denied to this child profile"}), 403

    # Get parent info
    child_age = age_calc(child.dob)
    parent = Parent.query.get(child.parent_id)
    parent_info = (
        {"id": parent.parent_id, "name": parent.name, "email": parent.email_id}
        if parent
        else None
    )

    # Skill progress
    all_skills = Skill.query.all()
    skills_progress = []
    for skill in all_skills:
        lessons = Lesson.query.filter_by(skill_id=skill.skill_id).all()
        lesson_ids = [l.lesson_id for l in lessons]

        lesson_started_count = len(lesson_ids)
        lesson_completed_count = LessonHistory.query.filter(
            LessonHistory.child_id == child_id, LessonHistory.lesson_id.in_(lesson_ids)
        ).count()
        quiz_attempted_count = (
            QuizHistory.query.join(Quiz)
            .filter(Quiz.lesson_id.in_(lesson_ids), QuizHistory.child_id == child_id)
            .count()
        )

        skills_progress.append(
            {
                "skill_id": str(skill.skill_id),
                "skill_name": skill.name,
                "lesson_started_count": lesson_started_count,
                "lesson_completed_count": lesson_completed_count,
                "quiz_attempted_count": quiz_attempted_count,
            }
        )

    # Points earned
    point_earned = []
    quiz_histories = (
        QuizHistory.query.join(Quiz).filter(QuizHistory.child_id == child_id).all()
    )
    for qh in quiz_histories:
        point_earned.append(
            {
                "point": qh.score,
                "date": (
                    qh.quiz.created_at.strftime("%Y-%m-%d")
                    if qh.quiz and qh.quiz.created_at
                    else "N/A"
                ),
            }
        )

    # Assessments (quizzes + activities)
    assessments = []
    for qh in quiz_histories:
        quiz = Quiz.query.get(qh.quiz_id)
        if quiz:
            assessments.append(
                {
                    "id": qh.quiz_history_id,
                    "skill_id": str(quiz.lesson.skill_id),
                    "assessment_type": "Quiz",
                    "title": quiz.quiz_name,
                    "date": (
                        quiz.created_at.strftime("%Y-%m-%d")
                        if quiz.created_at
                        else "N/A"
                    ),
                    "score": qh.score,
                    "max_score": quiz.points,
                }
            )

    activity_histories = (
        ActivityHistory.query.join(Activity).filter(Activity.child_id == child_id).all()
    )
    for ah in activity_histories:
        activity = ah.activity
        assessments.append(
            {
                "id": ah.activity_history_id,
                "skill_id": str(activity.lesson.skill_id) if activity.lesson else "N/A",
                "assessment_type": "Activity",
                "title": activity.name,
                "date": (
                    ah.created_at.strftime("%Y-%m-%d")
                    if hasattr(ah, "created_at") and ah.created_at
                    else "N/A"
                ),
                "score": "Pass",
                "max_score": "Pass",
            }
        )

    # Badges (encode images)
    badges = []
    badge_histories = (
        BadgeHistory.query.join(Badge).filter(BadgeHistory.child_id == child_id).all()
    )

    for bh in badge_histories:
        badge_img_base64 = ""

        if bh.badge and bh.badge.image:
            try:
                # Ensure image is in bytes, in case it's a memoryview
                image_data = bytes(bh.badge.image)
                badge_img_base64 = base64.b64encode(image_data).decode("utf-8")
            except Exception as e:
                print(f"[ERROR] Failed to encode image for badge_id={bh.badge_id}: {e}")

        badges.append(
            {
                "badge_id": str(bh.badge_id),
                "title": bh.badge.name if bh.badge else "",
                "image": badge_img_base64,
                "awarded_on": (
                    bh.created_at.strftime("%Y-%m-%d")
                    if hasattr(bh, "created_at") and bh.created_at
                    else "N/A"
                ),
            }
        )

    return (
        jsonify(
            {
                "info": {
                    "child_id": str(child.child_id),
                    "full_name": child.name,
                    "age": child_age,
                    "enrollment_date": (
                        child.enrollment_date.strftime("%Y-%m-%d")
                        if child.enrollment_date
                        else None
                    ),
                    "status": "Blocked" if child.is_blocked else "Active",
                    "parent": parent_info,
                },
                "skills_progress": skills_progress,
                "point_earned": point_earned,
                "assessments": sorted(
                    assessments, key=lambda x: x["date"], reverse=True
                ),
                "achievements": {"badges": badges, "streak": child.streak or 0},
            }
        ),
        200,
    )


def update_admin_email(current_user):
    data = request.get_json()
    new_email = data.get("email")

    if not new_email or "@" not in new_email:
        return jsonify({"error": "A valid email is required."}), 400

    # Check if the new email already exists in another admin account
    existing = Admin.query.filter(
        Admin.email_id == new_email, Admin.admin_id != current_user.admin_id
    ).first()
    if existing:
        return jsonify({"error": "An account with this email already exists."}), 409

    if not current_user:
        return jsonify({"error": "Admin not found."}), 404

    current_user.email_id = new_email
    db.session.commit()

    return jsonify({"message": "Email updated successfully."}), 200


def update_admin_password(current_user):
    data = request.get_json()

    old_password = data.get("oldPassword")
    new_password = data.get("newPassword")
    confirm_password = data.get("confirmPassword")

    if not old_password or not new_password or not confirm_password:
        return jsonify({"error": "All password fields are required."}), 400

    if new_password != confirm_password:
        return jsonify({"error": "New password & confirmation do not match."}), 400

    admin_id = current_user.admin_id
    admin = Admin.query.get(admin_id)

    if not admin:
        return jsonify({"error": "Admin not found."}), 404

    if not check_password_hash(admin.password, old_password):
        return jsonify({"error": "Old password is incorrect."}), 401

    admin.password = generate_password_hash(new_password)
    db.session.commit()

    return jsonify({"message": "Password updated successfully."}), 200


def block_child():
    data = request.get_json()
    child_id = data.get("id")

    if not child_id:
        return jsonify({"error": "Missing 'id' in request body"}), 400

    child = Child.query.get(child_id)
    if not child:
        return jsonify({"error": "Child not found"}), 404

    if child.is_blocked:
        return jsonify({"message": "Child is already blocked."}), 200

    child.is_blocked = True
    db.session.commit()

    return jsonify({"message": f"Child with ID {child_id} has been blocked."}), 200


def unblock_child():
    data = request.get_json()
    child_id = data.get("id")

    if not child_id:
        return jsonify({"error": "Missing 'id' in request body"}), 400

    child = Child.query.get(child_id)
    if not child:
        return jsonify({"error": "Child not found"}), 404

    if not child.is_blocked:
        return jsonify({"message": "Child is already unblocked."}), 200

    child.is_blocked = False
    db.session.commit()

    return jsonify({"message": f"Child with ID {child_id} has been unblocked."}), 200


def block_parent():
    data = request.get_json()
    parent_id = data.get("id")

    if not parent_id:
        return jsonify({"error": "Missing 'id' in request body"}), 400

    parent = Parent.query.get(parent_id)
    if not parent:
        return jsonify({"error": "Parent not found"}), 404

    if parent.is_blocked:
        return jsonify({"message": "Parent is already blocked."}), 200

    parent.is_blocked = True
    db.session.commit()

    return jsonify({"message": f"Parent with ID {parent_id} has been blocked."}), 200


def unblock_parent():
    data = request.get_json()
    parent_id = data.get("id")

    if not parent_id:
        return jsonify({"error": "Missing 'id' in request body"}), 400

    parent = Parent.query.get(parent_id)
    if not parent:
        return jsonify({"error": "Parent not found"}), 404

    if not parent.is_blocked:
        return jsonify({"message": "Parent is already unblocked."}), 200

    parent.is_blocked = False
    db.session.commit()

    return jsonify({"message": f"Parent with ID {parent_id} has been unblocked."}), 200


def update_activity(current_user, role):
    data = request.get_json()

    activity_id = data.get("id")
    if not activity_id:
        return jsonify({"error": "Missing required field: id"}), 400

    activity = Activity.query.get(activity_id)
    if not activity:
        return jsonify({"error": "Activity not found"}), 404

    image = data.get("image")
    title = data.get("title")
    description = data.get("description")
    instructions = data.get("instructions")
    difficulty = data.get("difficulty")
    lesson_id = data.get("lesson_id")

    # point = data.get("point")
    answer_format = data.get("answer_format")

    if image is not None:
        try:
            activity.image = base64.b64decode(image) if image else None
        except Exception:
            return jsonify({"error": "Invalid base64 image format"}), 400

    if title is not None:
        activity.name = title
    if description is not None:
        activity.description = description
    if instructions is not None:
        activity.instructions = instructions
    if difficulty is not None:
        activity.difficulty = difficulty
    if lesson_id is not None:
        activity.lesson_id = lesson_id

    # if point is not None:
    #     activity.points = point
    if answer_format is not None:
        allowed_formats = ["text", "image", "pdf"]
        if answer_format not in allowed_formats:
            return (
                jsonify(
                    {
                        "error": f"Invalid answer_format. Must be one of: {', '.join(allowed_formats)}"
                    }
                ),
                400,
            )
        activity.answer_format = answer_format

    db.session.commit()

    return (
        jsonify(
            {
                "message": "Activity updated successfully.",
                "id": activity.activity_id,
                "title": activity.name,
                "difficulty": activity.difficulty,
                # "points": activity.points,
                "answer_format": activity.answer_format,
            }
        ),
        200,
    )


def update_quiz(current_user, role):
    try:
        data = request.get_json()
    except Exception:
        return jsonify({"error": "Invalid JSON format"}), 400

    quiz_id = data.get("id")
    if not quiz_id:
        return jsonify({"error": "Missing quiz 'id'"}), 400

    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404

    title = data.get("title")
    description = data.get("description")
    difficulty = data.get("difficulty")
    points = data.get("point")
    time_duration = data.get("time_duration")
    image_base64 = data.get("image")
    questions = data.get("questions")
    lesson_id = data.get("lesson_id")

    if image_base64 is not None:
        try:
            quiz.image = base64.b64decode(image_base64) if image_base64 else None
        except Exception:
            return jsonify({"error": "Invalid base64 image"}), 400

    if title is not None:
        quiz.quiz_name = title
    if description is not None:
        quiz.description = description
    if difficulty is not None:
        quiz.difficulty = difficulty
    if points is not None:
        quiz.points = points
    if time_duration is not None:
        quiz.time_duration = time_duration
    if lesson_id is not None:
        quiz.lesson_id = lesson_id

    if questions is not None:
        if not isinstance(questions, list) or not questions:
            return jsonify({"error": "questions must be a non-empty list"}), 400

        questions_json = []
        answers_json = []

        for idx, question in enumerate(questions):
            q_text = question.get("question")
            opts = question.get("options", [])

            if not q_text or not isinstance(opts, list) or not opts:
                return (
                    jsonify({"error": f"Invalid question format at index {idx}"}),
                    400,
                )

            questions_json.append({"question": q_text, "options": opts})

            correct_answers = [
                opt["text"] for opt in opts if opt.get("isCorrect") is True
            ]

            if not correct_answers:
                return (
                    jsonify(
                        {"error": f"No correct answer specified for question: {q_text}"}
                    ),
                    400,
                )

            answers_json.append(
                {"question": q_text, "correct_answers": correct_answers}
            )

        quiz.questions = questions_json
        quiz.answers = answers_json

    db.session.commit()

    return (
        jsonify(
            {
                "message": "Quiz updated successfully",
                "id": quiz.quiz_id,
                "title": quiz.quiz_name,
                "difficulty": quiz.difficulty,
                "points": quiz.points,
                "time_duration": quiz.time_duration,
            }
        ),
        200,
    )


def update_lesson(current_user, role):
    try:
        data = request.get_json()
    except Exception:
        return jsonify({"error": "Invalid JSON format"}), 400

    lesson_id = data.get("id")
    if not lesson_id:
        return jsonify({"error": "Missing required field: id"}), 400

    lesson = Lesson.query.get(lesson_id)
    if not lesson:
        return jsonify({"error": f"Lesson with ID {lesson_id} not found"}), 404

    title = data.get("title")
    content_raw = data.get("content")
    image_base64 = data.get("image")
    description = data.get("description")
    curriculum_id = data.get("curriculum_id")

    if title is not None:
        lesson.title = title

    if description is not None:
        lesson.description = description

    if curriculum_id is not None:
        lesson.skill_id = curriculum_id

    if content_raw is not None:
        try:
            # content_json = json.loads(content_raw) if isinstance(content_raw, str) else content_raw
            lesson.content = content_raw
        except Exception:
            return (
                jsonify({"error": "Invalid content format. Must be valid JSON."}),
                400,
            )

    if image_base64 is not None:
        try:
            lesson.image = base64.b64decode(image_base64) if image_base64 else None
        except Exception:
            return jsonify({"error": "Invalid base64 image format"}), 400

    db.session.commit()

    return (
        jsonify(
            {
                "message": "Lesson updated successfully.",
                "id": lesson.lesson_id,
                "title": lesson.title,
            }
        ),
        200,
    )


def delete_badge(current_user, role):
    try:
        data = request.get_json()
    except Exception:
        return jsonify({"error": "Invalid JSON format"}), 400

    badge_id = data.get("id")

    if not badge_id:
        return jsonify({"error": "Missing 'id' field in request body"}), 400

    try:
        badge_id = int(badge_id)
    except ValueError:
        return jsonify({"error": "Invalid badge ID format."}), 400

    badge = Badge.query.get(badge_id)
    if not badge:
        return jsonify({"error": "Badge not found"}), 404

    db.session.delete(badge)
    db.session.commit()

    return jsonify({"message": f"Badge with ID {badge_id} has been deleted."}), 200


def delete_activity(current_user, role):
    try:
        data = request.get_json()
    except Exception:
        return jsonify({"error": "Invalid JSON format"}), 400

    activity_id = data.get("id")
    if not activity_id:
        return jsonify({"error": "Missing 'id' in request body"}), 400

    try:
        activity_id = int(activity_id)
    except ValueError:
        return jsonify({"error": "Activity ID must be a valid number."}), 400

    activity = Activity.query.get(activity_id)
    if not activity:
        return jsonify({"error": f"Activity with ID {activity_id} not found."}), 404

    db.session.delete(activity)
    db.session.commit()

    return (
        jsonify(
            {
                "message": f"Activity with ID {activity_id} has been deleted successfully."
            }
        ),
        200,
    )


def delete_quiz(current_user, role):
    try:
        data = request.get_json()
    except Exception:
        return jsonify({"error": "Invalid JSON format"}), 400

    quiz_id = data.get("id")
    if not quiz_id:
        return jsonify({"error": "Missing 'id' in request body"}), 400

    try:
        quiz_id = int(quiz_id)
    except ValueError:
        return jsonify({"error": "Quiz ID must be a valid number."}), 400

    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({"error": f"Quiz with ID {quiz_id} not found."}), 404

    db.session.delete(quiz)
    db.session.commit()

    return (
        jsonify({"message": f"Quiz with ID {quiz_id} has been deleted successfully."}),
        200,
    )


def delete_lesson(current_user, role):
    try:
        data = request.get_json()
    except Exception:
        return jsonify({"error": "Invalid JSON format"}), 400

    lesson_id = data.get("id")
    if not lesson_id:
        return jsonify({"error": "Missing 'id' in request body"}), 400

    try:
        lesson_id = int(lesson_id)
    except ValueError:
        return jsonify({"error": "Invalid lesson ID. Must be a number."}), 400

    lesson = Lesson.query.get(lesson_id)
    if not lesson:
        return jsonify({"error": f"Lesson with ID {lesson_id} not found."}), 404

    db.session.delete(lesson)
    db.session.commit()

    return (
        jsonify(
            {"message": f"Lesson with ID {lesson_id} has been deleted successfully."}
        ),
        200,
    )


def get_active_users_chart(current_user, role):
    try:
        end_date = datetime.today().date()
        start_date = end_date - timedelta(days=20)
        date_range = [
            start_date + timedelta(days=i)
            for i in range((end_date - start_date).days + 1)
        ]

        result = {
            "dates": [],
            "active_children": [],
            "active_parents": [],
            "new_children_signups": [],
            "new_parent_signups": [],
            "total_active_users": [],
        }

        for day in date_range:
            day_start = datetime.combine(day, datetime.min.time())
            day_end = datetime.combine(day, datetime.max.time())

            active_children_count = Child.query.filter(
                Child.last_login >= day_start, Child.last_login <= day_end
            ).count()

            active_parents_count = Parent.query.filter(
                Parent.children.any(
                    and_(Child.last_login >= day_start, Child.last_login <= day_end)
                )
            ).count()

            new_children = Child.query.filter(
                Child.enrollment_date >= day_start, Child.enrollment_date <= day_end
            ).count()

            new_parents = (
                Parent.query.join(Parent.children)
                .filter(
                    Child.enrollment_date >= day_start, Child.enrollment_date <= day_end
                )
                .distinct()
                .count()
            )

            result["dates"].append(day.strftime("%Y-%m-%d"))
            result["active_children"].append(active_children_count)
            result["active_parents"].append(active_parents_count)
            result["new_children_signups"].append(new_children)
            result["new_parent_signups"].append(new_parents)
            result["total_active_users"].append(
                active_children_count + active_parents_count
            )

        return jsonify(result), 200

    except Exception as e:
        return (
            jsonify(
                {"error": "Failed to generate active users chart", "details": str(e)}
            ),
            500,
        )


def get_skill_engagment_chart(current_user, role):
    # Prepare result: skill name by age group
    results = {"age_8_10": {}, "age_10_12": {}, "age_12_14": {}}

    all_skills = Skill.query.all()

    # For each skill, aggregate lessons and quizzes
    for skill in all_skills:
        skill_name = skill.name
        lesson_ids = [lesson.lesson_id for lesson in skill.lessons]
        quiz_ids = []
        for lesson in skill.lessons:
            quiz_ids += [quiz.quiz_id for quiz in lesson.quizzes]

        # Prepare counts per age group
        counts = {"age_8_10": 0, "age_10_12": 0, "age_12_14": 0}

        # Loop all children with DOB
        children = Child.query.filter(Child.dob != None).all()
        for child in children:
            today = date.today()
            age = age_calc(child.dob)
            group = None
            if 8 <= age <= 10:
                group = "age_8_10"
            elif 10 < age <= 12:
                group = "age_10_12"
            elif 12 < age <= 14:
                group = "age_12_14"
            if not group:
                continue

            lesson_count = LessonHistory.query.filter(
                LessonHistory.child_id == child.child_id,
                LessonHistory.lesson_id.in_(lesson_ids),
            ).count()
            quiz_count = QuizHistory.query.filter(
                QuizHistory.child_id == child.child_id,
                QuizHistory.quiz_id.in_(quiz_ids),
            ).count()
            counts[group] += lesson_count + quiz_count

        # Store per age group
        results["age_8_10"][skill_name] = counts["age_8_10"]
        results["age_10_12"][skill_name] = counts["age_10_12"]
        results["age_12_14"][skill_name] = counts["age_12_14"]

    # Format to contract spec
    return (
        jsonify(
            {
                "age_8_10": results["age_8_10"],
                "age_10_12": results["age_10_12"],
                "age_12_14": results["age_12_14"],
            }
        ),
        200,
    )


def get_badge_by_age_group_chart(current_user, role):
    # Get all badges
    badge_objs = Badge.query.all()
    results = []
    today = date.today()

    for badge in badge_objs:
        # Fetch all BadgeHistory for this badge, joined with Child for age computation
        badge_histories = BadgeHistory.query.filter_by(badge_id=badge.badge_id).all()

        age_counts = {"age_8_10": 0, "age_10_12": 0, "age_12_14": 0}

        for hist in badge_histories:
            child = Child.query.get(hist.child_id)
            if not child or not child.dob:
                continue
            age = age_calc(child.dob)
            if 8 <= age <= 10:
                age_counts["age_8_10"] += 1
            elif 10 < age <= 12:
                age_counts["age_10_12"] += 1
            elif 12 < age <= 14:
                age_counts["age_12_14"] += 1

        results.append(
            {
                "badge_name": badge.name,
                "age_8_10": age_counts["age_8_10"],
                "age_10_12": age_counts["age_10_12"],
                "age_12_14": age_counts["age_12_14"],
            }
        )

    return jsonify(results), 200


def get_learning_funnel_chart(current_user, role):
    try:
        # Users who started any skill (at least one lesson)
        started_lesson_subq = (
            db.session.query(LessonHistory.child_id).distinct().subquery()
        )

        user_started_skill = db.session.query(started_lesson_subq.c.child_id).count()

        # Total lessons completed (can be multiple per child)
        lessons_completed = db.session.query(LessonHistory).count()

        # Total quiz attempts
        quizzes_attempted = db.session.query(QuizHistory).count()

        # Badges earned (count of reward history)
        badges_earned = db.session.query(BadgeHistory).count()

        return (
            jsonify(
                [
                    {
                        "user_started_skill": user_started_skill,
                        "lessons_completed": lessons_completed,
                        "quizzes_attempted": quizzes_attempted,
                        "badges_earned": badges_earned,
                    }
                ]
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        return (
            jsonify({"error": "Failed to generate funnel metrics", "details": str(e)}),
            500,
        )


def get_age_group_distribution_chart():
    today = date.today()
    age_brackets = [
        ("age_8_10", 8, 10),
        ("age_10_12", 10, 12),
        ("age_12_14", 12, 14),
    ]

    skills = Skill.query.all()
    result = []

    for skill in skills:
        skill_obj = {
            "skill_id": str(skill.skill_id),
            "skill_name": skill.name,
            "lesson_started_count": {},
            "lesson_completed_count": {},
            "quiz_attempted_count": {},
        }

        lessons = Lesson.query.filter_by(skill_id=skill.skill_id).all()
        lesson_ids = [lesson.lesson_id for lesson in lessons]

        quizzes = Quiz.query.filter(Quiz.lesson_id.in_(lesson_ids)).all()
        quiz_ids = [quiz.quiz_id for quiz in quizzes]

        for bracket_label, min_age, max_age in age_brackets:
            # Get children in this age bracket
            children_in_bracket = Child.query.filter(Child.dob != None).all()
            children_ids = [
                child.child_id
                for child in children_in_bracket
                if min_age
                <= (
                    today.year
                    - child.dob.year
                    - ((today.month, today.day) < (child.dob.month, child.dob.day))
                )
                <= max_age
            ]

            # Lessons started (unique children who started any lesson in this skill and age bracket)
            started_count = (
                LessonHistory.query.filter(
                    LessonHistory.child_id.in_(children_ids),
                    LessonHistory.lesson_id.in_(lesson_ids),
                )
                .distinct(LessonHistory.child_id)
                .count()
            )

            # Lessons completed (total completed records in bracket, or you may want distinct by lesson/child)
            completed_count = LessonHistory.query.filter(
                LessonHistory.child_id.in_(children_ids),
                LessonHistory.lesson_id.in_(lesson_ids),
            ).count()

            # Quizzes attempted (total attempted in bracket)
            quiz_attempted = QuizHistory.query.filter(
                QuizHistory.child_id.in_(children_ids),
                QuizHistory.quiz_id.in_(quiz_ids),
            ).count()

            skill_obj["lesson_started_count"][bracket_label] = started_count
            skill_obj["lesson_completed_count"][bracket_label] = completed_count
            skill_obj["quiz_attempted_count"][bracket_label] = quiz_attempted

        result.append(skill_obj)

    return jsonify(result), 200


def update_personal_details(current_user):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()

    # Check if both fields are present
    if not name or not email:
        return jsonify({"error": "Both name and email are required."}), 400

    parent_id = current_user.parent_id
    parent = Parent.query.get(parent_id)
    if not parent:
        return jsonify({"error": "Parent not found."}), 404

    # Check for email uniqueness if it's changed
    if parent.email_id != email:
        existing = Parent.query.filter(
            Parent.email_id == email, Parent.parent_id != parent_id
        ).first()
        if existing:
            return (
                jsonify({"error": "Email already registered to another account."}),
                409,
            )

    # Update fields
    parent.name = name
    parent.email_id = email
    db.session.commit()

    return (
        jsonify(
            {
                "id": parent.parent_id,
                "name": parent.name,
                "email": parent.email_id,
                "message": "Personal details updated successfully.",
            }
        ),
        200,
    )


def update_parent_password(current_user):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    old_password = data.get("oldPassword")
    new_password = data.get("newPassword")
    confirm_password = data.get("confirmPassword")

    # Validate required fields
    if not all([old_password, new_password, confirm_password]):
        return (
            jsonify(
                {
                    "error": "All fields (oldPassword, newPassword, confirmPassword) are required."
                }
            ),
            400,
        )

    if new_password != confirm_password:
        return (
            jsonify({"error": "New password and confirm password do not match."}),
            400,
        )

    if len(new_password) < 4:
        return (
            jsonify({"error": "New password must be at least 4 characters long."}),
            400,
        )

    parent = Parent.query.get(current_user.parent_id)
    if not parent:
        return jsonify({"error": "Parent not found"}), 404

    if not check_password_hash(parent.password, old_password):
        return jsonify({"error": "Old password is incorrect."}), 401

    if check_password_hash(parent.password, new_password):
        return (
            jsonify(
                {"error": "New password must be different from the current password."}
            ),
            409,
        )

    parent.password = generate_password_hash(new_password)
    db.session.commit()

    return jsonify({"message": "Password updated successfully."}), 200


def post_feedback(current_user, role):
    data = request.get_json()

    skill_type = data.get("skill_type")
    item_id = data.get("id")
    feedback_text = data.get("text", "").strip()

    if skill_type not in ("Quiz", "Activity"):
        return (
            jsonify({"error": "Invalid skill_type. Must be 'Quiz' or 'Activity'."}),
            400,
        )

    if not item_id or not isinstance(item_id, int):
        return jsonify({"error": "Valid numeric 'id' is required."}), 400

    if not feedback_text:
        return jsonify({"error": "Feedback text cannot be empty."}), 400

    try:
        if skill_type == "Quiz":
            quiz_history = QuizHistory.query.get(item_id)
            if not quiz_history:
                return jsonify({"error": "Quiz attempt not found."}), 404
            quiz_history.feedback = feedback_text

        elif skill_type == "Activity":
            activity_history = ActivityHistory.query.get(item_id)
            if not activity_history:
                return jsonify({"error": "Activity attempt not found."}), 404
            activity_history.feedback = feedback_text

        db.session.commit()

        return jsonify({"message": "Feedback submitted successfully."}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error occurred", "details": str(e)}), 500


def get_skills():
    skills = Skill.query.all()
    response = []

    for skill in skills:
        response.append(
            {
                "id": skill.skill_id,
                "name": skill.name,
                "description": skill.description,
            }
        )

    return jsonify(response), 200


def get_children_by_age_groups():
    # Calculate age from DOB using SQLite-compatible SQL
    age = cast(func.strftime("%Y", "now"), Integer) - cast(
        func.strftime("%Y", Child.dob), Integer
    )

    age_8_10 = func.sum(case((age.between(8, 9), 1), else_=0)).label("age_8_10")

    age_10_12 = func.sum(case((age.between(10, 11), 1), else_=0)).label("age_10_12")

    age_12_14 = func.sum(case((age.between(12, 13), 1), else_=0)).label("age_12_14")

    result = db.session.query(age_8_10, age_10_12, age_12_14).one()

    return jsonify(
        {
            "age_8_10": int(result.age_8_10),
            "age_10_12": int(result.age_10_12),
            "age_12_14": int(result.age_12_14),
        }
    )


def get_lesson_details_by_id(lesson_id: int):
    """
    get lesson details for a practicular lesson using id
    """
    if not lesson_id:
        return jsonify({"message": "Lesson id missing"}), 400
    lesson: Lesson = Lesson.query.filter(Lesson.lesson_id == lesson_id).first_or_404()

    return (
        jsonify(
            {
                "id": lesson.lesson_id,
                "skill_id": lesson.skill_id,
                "title": lesson.title,
                "description": lesson.description,
                "content": lesson.content,
            }
        ),
        200,
    )


def get_activity_details_by_id(activity_id: int):
    """
    get lesson details for a practicular lesson using id
    """
    if not activity_id:
        return jsonify({"message": "Activity id missing"}), 400
    act: Activity = Activity.query.filter(
        Activity.activity_id == activity_id
    ).first_or_404()

    return (
        jsonify(
            {
                "id": act.activity_id,
                "title": act.name,
                "description": act.description,
                "instructions": act.instructions,
                "difficulty": act.difficulty,
                "lesson_id": act.lesson_id,
                "answer_format": act.answer_format,
            }
        ),
        200,
    )


def get_quiz_details_by_id(quiz_id: int):
    """
    get lesson details for a practicular lesson using id
    """
    if not quiz_id:
        return jsonify({"message": "quiz_id missing"}), 400
    quiz: Quiz = Quiz.query.filter(Quiz.quiz_id == quiz_id).first_or_404()

    return (
        jsonify(
            {
                "id": quiz.quiz_id,
                "title": quiz.quiz_name,
                "description": quiz.description,
                "difficulty": quiz.difficulty,
                "lesson_id": quiz.lesson_id,
                "points": quiz.points,
                "questions": quiz.questions,
                "time_duration": quiz.time_duration,
            }
        ),
        200,
    )
