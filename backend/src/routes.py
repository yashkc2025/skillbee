from flask import Blueprint, request, jsonify
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
from .db import db
from .demoData import createDummyData
from functools import wraps
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta
from flask_apscheduler import APScheduler
from .controllers import (
    admin_child_profile,
    admin_create,
    get_active_users_chart,
    get_activity_by_parent,
    get_age_group_distribution_chart,
    get_badge_by_age_group_chart,
    get_learning_funnel_chart,
    get_settings,
    get_skill_engagment_chart,
    get_skills,
    parent_regisc,
    child_regisc,
    admin_loginc,
    parent_loginc,
    child_loginc,
    get_auser,
    get_child_dashboard_stats,
    get_child_heatmap,
    get_leaderboard,
    get_user_skill_progress,
    get_user_badges,
    get_curriculums_for_child,
    get_skill_lessons,
    get_lesson_details,
    mark_lesson_completed,
    get_lesson_activities,
    get_lesson_quizzes,
    get_activity_details,
    post_feedback,
    submit_activity,
    get_activity_history,
    get_activity_submission,
    get_quiz_questions,
    submit_quiz,
    get_child_quiz_history,
    get_quiz_history,
    get_child_profile_controller,
    update_child_profile,
    change_child_password,
    child_profile_image,
    get_child_badges,
    get_children,
    get_parents,
    get_lessons,
    get_quizzes,
    get_activities,
    get_badges,
    create_child,
    create_quiz,
    create_activity,
    create_badge,
    create_lesson,
    update_activity,
    update_admin_email,
    update_admin_password,
    update_lesson,
    update_parent_password,
    update_personal_details,
    update_quiz,
    block_child,
    unblock_child,
    block_parent,
    unblock_parent,
    delete_activity,
    delete_badge,
    delete_lesson,
    delete_quiz,
    get_children_by_age_groups,
    get_lesson_details_by_id,
    get_activity_details_by_id,
    get_quiz_details_by_id,
    update_settings,
)

scheduler = APScheduler()

api = Blueprint("api", __name__)


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
        id="cleanup_sessions",
        func=wrapped_cleanup,
        trigger="interval",
        hours=1,
        max_instances=1,
        next_run_time=datetime.now() + timedelta(hours=1),
    )

    # Start the scheduler
    scheduler.start()


def cleanup_expired_sessions():
    try:
        expiry_time = datetime.now() - timedelta(hours=3)
        expired_sessions = [
            session
            for session in Session.query.all()
            if datetime.fromisoformat(session.session_information["login_time"])
            < expiry_time
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
            if "Authorization" in request.headers:
                token = request.headers["Authorization"].split(" ")[-1]
                print(token)

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


### Dummy Data Route ###


@api.route("/dummyData", methods=["GET"])
def dummyData():
    createDummyData()
    return "Dummy data has been created!"


### User Registration Routes ###


@api.route("/auth/parent_register", methods=["POST"])
def parent_register():
    return parent_regisc(request)


@api.route("/auth/children_register", methods=["POST"])
def child_register():
    return child_regisc(request)


@api.route("/auth/admin_create", methods=["POST"])
def admin_create_route():
    return admin_create()


### User Login Routes ###


@api.route("/auth/admin_login", methods=["POST"])
def admin_login():
    return admin_loginc()


@api.route("/auth/parent_login", methods=["POST"])
def parent_login():
    return parent_loginc(request)


@api.route("/auth/children_login", methods=["POST"])
def child_login():
    return child_loginc(request)


@api.route("/auth/get_user", methods=["GET"])
@token_required(allowed_roles=["admin", "parent", "child"])
def get_user(current_user, role):
    return get_auser(current_user, role)


### Children Dashboard Routes ###


@api.route("/child_dashboard_stats", methods=["GET"])
@token_required(allowed_roles=["child"])
def child_dashboard_stats(current_user, role):
    return get_child_dashboard_stats(current_user.child_id)


@api.route("/child_heatmap", methods=["GET"])
@token_required(allowed_roles=["child"])
def child_heatmap(current_user, role):
    return get_child_heatmap(current_user.child_id)


@api.route("/child_leaderboard", methods=["GET"])
@token_required(allowed_roles=["child"])
def child_leaderboard(current_user, role):
    return get_leaderboard(current_user.child_id)


### Admin and Parent Routes ###


@api.route("/children", methods=["GET"])
@token_required(allowed_roles=["admin", "parent"])
def get_child(current_user, role):
    return get_children(current_user, role)


@api.route("/parents", methods=["GET"])
@token_required(allowed_roles=["admin"])
def get_parent(current_user, role):
    return get_parents(current_user.admin_id, role)


@api.route("/lessons", methods=["GET"])
@token_required(allowed_roles=["admin", "parent"])
def get_lesson(current_user, role):
    return get_lessons(current_user, role)


@api.route("/quizzes", methods=["GET"])
@token_required(allowed_roles=["admin", "parent"])
def get_quiz(current_user, role):
    return get_quizzes(current_user, role)


@api.route("/activities", methods=["GET"])
@token_required(allowed_roles=["admin", "parent"])
def get_activity(current_user, role):
    return get_activities(current_user, role)


@api.route("/badges", methods=["GET"])
@token_required(allowed_roles=["admin", "parent"])
def get_badge(current_user, role):
    return get_badges(current_user, role)


@api.route("/parent/children", methods=["POST"])
@token_required(allowed_roles=["parent"])
def parent_children(current_user, role):
    return create_child(current_user, role)


@api.route("/admin/badge", methods=["POST"])
@token_required(allowed_roles=["admin"])
def admin_badge(current_user, role):
    return create_badge(current_user.admin_id, role)


@api.route("/admin/activity", methods=["POST"])
@token_required(allowed_roles=["admin", "parent"])
def admin_activity(current_user, role):
    return create_activity(current_user)


@api.route("/admin/lesson", methods=["POST"])
@token_required(allowed_roles=["admin"])
def admin_lesson(current_user, role):
    return create_lesson(current_user.admin_id, role)


@api.route("/admin/quiz", methods=["POST"])
@token_required(allowed_roles=["admin"])
def admin_quiz(current_user, role):
    return create_quiz(current_user.admin_id, role)


@api.route("/admin/update_email", methods=["PUT"])
@token_required(allowed_roles=["admin"])
def admin_email(current_user, role):
    return update_admin_email(current_user.admin_id, role)


@api.route("/admin/update_password", methods=["PUT"])
@token_required(allowed_roles=["admin"])
def admin_password(current_user, role):
    return update_admin_password(current_user)


@api.route("/admin/block_children", methods=["PUT"])
@token_required(allowed_roles=["admin"])
def block_children(current_user, role):
    return block_child()


@api.route("/admin/unblock_children", methods=["PUT"])
@token_required(allowed_roles=["admin"])
def unblock_children(current_user, role):
    return unblock_child()


@api.route("/admin/block_parent", methods=["PUT"])
@token_required(allowed_roles=["admin"])
def block_parents(current_user, role):
    return block_parent()


@api.route("/admin/unblock_parent", methods=["PUT"])
@token_required(allowed_roles=["admin"])
def unblock_parents(current_user, role):
    return unblock_parent()


@api.route("/admin/activity", methods=["PUT"])
@token_required(allowed_roles=["admin", "parent"])
def update_activities(current_user, role):
    return update_activity()


@api.route("/admin/quiz", methods=["PUT"])
@token_required(allowed_roles=["admin"])
def update_quizzes(current_user, role):
    return update_quiz(current_user.admin_id, role)


@api.route("/admin/lesson", methods=["PUT"])
@token_required(allowed_roles=["admin"])
def update_lessons(current_user, role):
    return update_lesson(current_user.admin_id, role)


@api.route("/admin/badge", methods=["DELETE"])
@token_required(allowed_roles=["admin"])
def delete_badges(current_user, role):
    return delete_badge(current_user.admin_id, role)


@api.route("/admin/activity", methods=["DELETE"])
@token_required(allowed_roles=["admin", "parent"])
def delete_activities(current_user, role):
    return delete_activity()


@api.route("/admin/lesson", methods=["DELETE"])
@token_required(allowed_roles=["admin"])
def delete_lessons(current_user, role):
    return delete_lesson(current_user.admin_id, role)


@api.route("/admin/quiz", methods=["DELETE"])
@token_required(allowed_roles=["admin"])
def delete_quizzes(current_user, role):
    return delete_quiz(current_user.admin_id, role)


@api.route("/children/profile", methods=["GET"])
@token_required(allowed_roles=["admin", "parent", "child"])
def children_profile(current_user, role):
    return admin_child_profile(current_user, role)


@api.route("/admin/age_distribution_chart", methods=["GET"])
@token_required(allowed_roles=["admin", "child"])
def get_age_distribution_chart(current_user, role):
    return get_age_group_distribution_chart()


@api.route("/admin/learning_funnel_chart", methods=["GET"])
@token_required(allowed_roles=["admin"])
def get_funnel_chart(current_user, role):
    return get_learning_funnel_chart(current_user.admin_id, role)


@api.route("/admin/badge_by_age_group_chart", methods=["GET"])
@token_required(allowed_roles=["admin"])
def get_badge_by_age_group(current_user, role):
    return get_badge_by_age_group_chart(current_user.admin_id, role)


@api.route("/admin/skill_engagment_chart", methods=["GET"])
@token_required(allowed_roles=["admin"])
def get_skill_engagement(current_user, role):
    return get_skill_engagment_chart(current_user.admin_id, role)


@api.route("/admin/active_users_chart", methods=["GET"])
@token_required(allowed_roles=["admin"])
def get_active_users(current_user, role):
    return get_active_users_chart(current_user.admin_id, role)


@api.route("/feedback", methods=["POST"])
@token_required(allowed_roles=["parent"])
def feedback(current_user, role):
    return post_feedback(current_user.parent_id, role)


@api.route("/parent/update_personal_details", methods=["PUT"])
@token_required(allowed_roles=["parent"])
def update_parent_details():
    return update_personal_details()


@api.route("/parent/update_password", methods=["PUT"])
@token_required(allowed_roles=["parent"])
def parent_password(current_user, role):
    return update_parent_password(current_user)


### Children Routes ###


@api.route("/api/child/<int:child_id>/curriculums", methods=["GET"])
@token_required(allowed_roles=["child"])
def get_curr(current_user, role, child_id):
    return get_curriculums_for_child(current_user.child_id)


@api.route("/api/child/curriculum/<int:curriculum_id>/lessons", methods=["GET"])
@token_required(allowed_roles=["child"])
def get_skill_lessons_route(curriculum_id, current_user, role):
    return get_skill_lessons(current_user.child_id, curriculum_id)


@api.route("/api/child/lesson/<int:lesson_id>", methods=["GET"])
@token_required(allowed_roles=["child"])
def get_lesson_details_route(lesson_id, current_user, role):
    return get_lesson_details(current_user.child_id, lesson_id)


@api.route("/api/child/lesson/<int:lesson_id>/mark-read", methods=["POST"])
@token_required(allowed_roles=["child"])
def mark_lesson_complete_route(lesson_id, current_user, role):
    completed_at = request.json.get("completed_at") if request.json else None
    return mark_lesson_completed(current_user.child_id, lesson_id, completed_at)


@api.route("/api/child/lesson/<int:lesson_id>/activities", methods=["GET"])
@token_required(allowed_roles=["child"])
def get_lesson_activities_route(lesson_id, current_user, role):
    return get_lesson_activities(current_user.child_id, lesson_id)


@api.route("/api/child/activity/<int:activity_id>", methods=["GET"])
@token_required(allowed_roles=["child"])
def get_activity_details_route(activity_id, current_user, role):
    return get_activity_details(current_user.child_id, activity_id)


@api.route("/api/child/activity/<int:activity_id>/submit", methods=["POST"])
@token_required(allowed_roles=["child"])
def submit_activity_route(activity_id, current_user, role):
    return submit_activity(current_user.child_id, activity_id)


@api.route("/api/child/activity/<int:activity_id>/history", methods=["GET"])
@token_required(allowed_roles=["child"])
def get_activity_history_route(activity_id, current_user, role):
    return get_activity_history(current_user.child_id, activity_id)


@api.route("/api/child/activity/history/<int:activity_history_id>", methods=["GET"])
@token_required(allowed_roles=["child"])
def get_activity_submission_route(activity_history_id, current_user, role):
    return get_activity_submission(current_user.child_id, activity_history_id)


@api.route("/api/child/lesson/<int:lesson_id>/quizzes", methods=["GET"])
@token_required(allowed_roles=["child"])
def get_quizzes_route(lesson_id, current_user, role):
    return get_lesson_quizzes(current_user.child_id, lesson_id)


@api.route(
    "/api/child/curriculum/<int:curriculum_id>/lesson/<int:lesson_id>/quiz/<int:quiz_id>",
    methods=["GET"],
)
@token_required(allowed_roles=["child"])
def get_quiz_questions_route(curriculum_id, lesson_id, quiz_id, current_user, role):
    return get_quiz_questions(curriculum_id, lesson_id, quiz_id)


@api.route("/api/child/quizzes/<int:quiz_id>/submit", methods=["POST"])
@token_required(allowed_roles=["child"])
def submit_quiz_route(quiz_id, current_user, role):
    return submit_quiz(current_user.child_id, quiz_id)


@api.route(
    "/api/child/curriculum/<int:curriculum_id>/lesson/<int:lesson_id>/quiz/<int:quiz_id>/quiz_history/<int:quiz_history_id>",
    methods=["GET"],
)
@token_required(allowed_roles=["child"])
def get_quiz_history_route_with_history_id(
    curriculum_id, lesson_id, quiz_id, quiz_history_id, current_user, role
):
    return get_child_quiz_history(curriculum_id, lesson_id, quiz_id, quiz_history_id)


@api.route("/api/child/quiz/<int:quiz_id>/history", methods=["GET"])
@token_required(allowed_roles=["child"])
def get_quiz_history_route(quiz_id, current_user, role):
    return get_quiz_history(current_user.child_id, quiz_id)


@api.route("/api/child/setting", methods=["GET"])
@token_required(allowed_roles=["child"])
def get_child_profile_route(current_user, role):
    return get_child_profile_controller(current_user.child_id)


@api.route("/api/child/update_profile", methods=["PUT"])
@token_required(allowed_roles=["child"])
def update_child_profile_route(current_user, role):
    return update_child_profile(current_user.child_id)


@api.route("/api/child/change_password", methods=["PUT"])
@token_required(allowed_roles=["child"])
def change_child_password_route(current_user, role):
    return change_child_password(current_user.child_id)


@api.route("/api/child/profile_image", methods=["GET", "POST"])
@token_required(allowed_roles=["child"])
def child_profile_image_route(current_user, role):
    return child_profile_image(current_user.child_id)


@api.route("/child_badges", methods=["GET"])
@token_required(allowed_roles=["child"])
def child_badges(current_user, role):
    return get_child_badges(current_user.child_id)


@api.route("/skill_categories", methods=["GET"])
@token_required(allowed_roles=["child"])
def get_skill_categories(current_user, role):
    return get_user_skill_progress(current_user.child_id)


@api.route("/user_badges", methods=["GET"])
@token_required(allowed_roles=["child"])
def user_badges(current_user, role):
    return get_user_badges(current_user.child_id)


@api.route("/skills", methods=["GET"])
@token_required(allowed_roles=["admin", "parent"])
def get_sklills_route(current_user, role):
    return get_skills()


@api.route("/age_group_chart", methods=["GET"])
@token_required(allowed_roles=["admin", "parent"])
def age_group_chart(current_user, role):
    return get_children_by_age_groups()


@api.route("/admin/lesson/<int:lesson_id>", methods=["GET"])
@token_required(allowed_roles=["admin"])
def get_lesson_by_id(lesson_id, current_user, role):
    return get_lesson_details_by_id(lesson_id)


@api.route("/admin/activity/<int:activity_id>", methods=["GET"])
@token_required(allowed_roles=["admin", "parent"])
def get_act_by_id(activity_id, current_user, role):
    return get_activity_details_by_id(activity_id)


@api.route("/admin/quiz/<int:quiz_id>", methods=["GET"])
@token_required(allowed_roles=["admin"])
def get_quiz_by_id(quiz_id, current_user, role):
    return get_quiz_details_by_id(quiz_id)


@api.route("/parent/activity", methods=["GET"])
@token_required(allowed_roles=["parent"])
def get_parent_activity(current_user, role):
    return get_activity_by_parent(current_user.parent_id)


@api.route("/settings", methods=["GET"])
@token_required(allowed_roles=["parent", "admin"])
def get_settings_parent_or_admin(current_user, role):
    user_id = getattr(current_user, "admin_id", None) or getattr(
        current_user, "parent_id", None
    )

    return get_settings(user_id, role)


@api.route("/settings", methods=["PUT"])
@token_required(allowed_roles=["parent", "admin"])
def put_settings_parent_or_admin(current_user, role):
    user_id = getattr(current_user, "admin_id", None) or getattr(
        current_user, "parent_id", None
    )

    return update_settings(user_id, role)
