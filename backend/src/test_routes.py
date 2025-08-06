import json
import pytest
from flask import Flask
from .routes import api
from flasgger import Swagger
from . import create_app
from .controllers import admin_create
from datetime import datetime, date
from unittest.mock import patch
from types import SimpleNamespace

# Swagger(api)
app=create_app()

# Testing functions for registration apis

def test_parent_register_success():
    # to test the registration function of parent success
    tester = app.test_client()
    response = tester.post('/auth/parent_register', json={
        "name": "Test Parent",
        "email": "testparent@example.com",
        "password": "1234",
        "profile_image": ""
    })
    assert response.status_code in (201, 409)
    data = response.get_json()
    assert "user" in data or "error" in data

def test_parent_register_failure():
    # to test the registration function of parent fail
    tester = app.test_client()
    response = tester.post('/auth/parent_register', json={
        "name": "Test Parent",
        "email": "", 
        "password": "1234",
        "profile_image": ""
    })
    assert response.status_code in (400, 404)
    data = response.get_json()
    assert "error" in data

def test_children_register_success():
    # to test the registration function of child success
        with app.app_context():
            tester = app.test_client()
            response = tester.post('/auth/children_register', json={
                "name": "test child",
                "email": "testchild@gmail.com",
                "password": "abcdef",
                "username": "ubbbbbbb",
                "dob": "2014-09-09",
                "school": "abcd",
                "profile_image": ""
            })
            assert response.status_code in (201, 409)
            data = response.get_json()
            assert "user" in data or "error" in data

def test_children_register_failure():
    # to test the registration function of child fail
    tester = app.test_client()
    response = tester.post('/auth/children_register', json={
    "name":"test child",
    "email": "",
    "password": "",
    "username": "ubbbbbbb",
    "dob": "2009-09-09",
    "school": "sphs",
    "profile_image": ""
})
    assert response.status_code in (400, 404)
    data = response.get_json()
    assert "error" in data

# Testing functions for login apis

def test_parent_login_success():
    """ Test successful login of a registered parent user. """
    tester = app.test_client()

    response = tester.post('/auth/parent_login', json={
        "email": "testparent@example.com",
        "password": "1234"
    })

    assert response.status_code == 200
    data = response.get_json()
    assert "user" in data or "error" in data
    

def test_parent_login_failure():
    """ Test failed login attempt due to missing email field."""
    
    tester = app.test_client()

    response = tester.post('/auth/parent_login', json={
        "email": "",
        "password": "1234"
    })
    assert response.status_code in (400, 401)
    data = response.get_json()
    assert "user" in data or "error" in data
    
    response = tester.post('/auth/parent_login', json={
        "email": "wrong_email",
        "password": "random_password"
    })
    assert response.status_code == 401
    data = response.get_json()
    assert "user" in data or "error" in data
    
    
def test_children_login_success():
    """ Test successful login of a registered child. """
    
    with app.app_context():
        tester = app.test_client()
        response = tester.post('/auth/children_login', json={
            "email_or_username": "testchild@gmail.com",
            "password": "abcdef"
        })
        assert response.status_code == 200
        data = response.get_json()
        assert "user" in data
        assert "session" in data
        assert "token" in data["session"]
    
    
def test_children_login_failure():
    """ Test failed login attempt of a children due to missing or invalid fields. """
    
    tester = app.test_client()
    
    response = tester.post('/auth/children_login', json={
        "email_or_username": "",
        "password": "abcdef"
    })
    assert response.status_code in (400, 401)
    data = response.get_json()
    assert "error" in data

    response = tester.post('/auth/children_login', json={
        "email_or_username": "nonexistent_user",
        "password": "wrongpass"
    })
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data

def test_admin_login_success():
    # test to see if admin login works fine
    with app.app_context():
        admin_create()

    tester = app.test_client()
    response = tester.post('/auth/admin_login', json={
        "email_id": "admin@gmail.com",
        "password": "1234"
    })

    assert response.status_code in (201,200)
    data = response.get_json()
    assert "session" in data
    assert "token" in data["session"]
    assert "login_time" in data["session"]

def test_admin_login_failure_wrong_password():
    # test to check admin wrong creds
    with app.app_context():
        admin_create()
    tester = app.test_client()
    response = tester.post('/auth/admin_login', json={
        "email_id": "admin@gmail.com",
        "password": "wrongpassword"
    })

    assert response.status_code == 401
    data = response.get_json()
    assert data["error"] == "Invalid email or password"


def test_admin_login_missing_fields():
    # test to check teh admin database error
    tester = app.test_client()
    response = tester.post('/auth/admin_login', json={
        "email_id": ""
    })
    assert response.status_code == 500  
    data = response.get_json()
    assert data["error"] == "Missing email or password"


# @pytest.fixture
# def client():
#     with app.test_client() as client:
#         with app.app_context():
#             yield client

# class TestGetAUser:

#     @patch('src.routes.Session.query')
#     def test_missing_auth(self, mock_sess_query, client):
#         response = client.get('/auth/get_user')
#         assert response.status_code == 403
#         data = response.get_json()
#         assert data["error"] == "Missing or malformed token"

#     @patch('src.routes.Session.query')
#     def test_invalid_token(self, mock_sess_query, client):
#         mock_sess_query.filter_by.return_value = SimpleNamespace(first=lambda: None)

#         response = client.get('/auth/get_user', headers={
#             "Authorization": "Bearer invalid_token"
#         })

#         assert response.status_code == 401
#         data = response.get_json()
#         assert data["error"] == "Invalid credentials"

#     @patch('src.routes.Session.query')
#     @patch('src.routes.Child.query')
#     def test_success_child(self, mock_child_query, mock_sess_query, client):
#         session_mock = SimpleNamespace(
#             session_information={
#                 "child_id": 1,
#                 "email": "child@example.com",
#                 "login_time": "2024-06-20T12:00:00"
#             }
#         )
#         child_mock = SimpleNamespace(
#             child_id=1,
#             name="Test Child",
#             username="testchild",
#             email_id="child@example.com",
#             dob=date(2010, 5, 15),
#             school="Greenwood High",
#             profile_image=None
#         )
#         mock_sess_query.filter_by.return_value = SimpleNamespace(first=lambda: session_mock)
#         mock_child_query.get.return_value = child_mock

#         response = client.get('/auth/get_user', headers={
#             "Authorization": "Bearer any_token"
#         })

#         assert response.status_code == 200
#         data = response.get_json()["user"]
#         assert data["username"] == "testchild"
#         assert data["role"] == "child"

#     @patch('src.routes.Session.query')
#     @patch('src.routes.Child.query')
#     def test_child_not_found(self, mock_child_query, mock_sess_query, client):
#         session_mock = SimpleNamespace(
#             session_information={
#                 "child_id": 1,
#                 "email": "child@example.com",
#                 "login_time": "2024-06-20T12:00:00"
#             }
#         )
#         mock_sess_query.filter_by.return_value = SimpleNamespace(first=lambda: session_mock)
#         mock_child_query.get.return_value = None

#         response = client.get('/auth/get_user', headers={
#             "Authorization": "Bearer any_token"
#         })

#         assert response.status_code == 404
#         data = response.get_json()
#         assert data["error"] == "User not found"

#     @patch('src.routes.Session.query')
#     @patch('src.routes.Parent.query')
#     def test_success_parent(self, mock_parent_query, mock_sess_query, client):
#         session_mock = SimpleNamespace(
#             session_information={
#                 "parent_id": 10,
#                 "email": "parent@example.com",
#                 "login_time": "2024-06-20T12:00:00"
#             }
#         )
#         parent_mock = SimpleNamespace(
#             parent_id=10,
#             name="Test Parent",
#             email_id="parent@example.com",
#             profile_image=None
#         )
#         mock_sess_query.filter_by.return_value = SimpleNamespace(first=lambda: session_mock)
#         mock_parent_query.get.return_value = parent_mock

#         response = client.get('/auth/get_user', headers={
#             "Authorization": "Bearer any_token"
#         })

#         assert response.status_code == 200
#         data = response.get_json()["user"]
#         assert data["name"] == "Test Parent"
#         assert data["role"] == "parent"

#     @patch('src.routes.Session.query')
#     @patch('src.routes.Parent.query')
#     def test_parent_not_found(self, mock_parent_query, mock_sess_query, client):
#         session_mock = SimpleNamespace(
#             session_information={
#                 "parent_id": 10,
#                 "email": "parent@example.com",
#                 "login_time": "2024-06-20T12:00:00"
#             }
#         )
#         mock_sess_query.filter_by.return_value = SimpleNamespace(first=lambda: session_mock)
#         mock_parent_query.get.return_value = None

#         response = client.get('/auth/get_user', headers={
#             "Authorization": "Bearer any_token"
#         })

#         assert response.status_code == 404
#         data = response.get_json()
#         assert data["error"] == "User not found"

#     @patch('src.routes.Session.query')
#     def test_invalid_session_data(self, mock_sess_query, client):
#         session_mock = SimpleNamespace(
#             session_information={
#                 "email": "unknown@example.com",
#                 "login_time": "2024-06-20T12:00:00"
#                 # No child_id or parent_id
#             }
#         )
#         mock_sess_query.filter_by.return_value = SimpleNamespace(first=lambda: session_mock)

#         response = client.get('/auth/get_user', headers={
#             "Authorization": "Bearer any_token"
#         })

#         assert response.status_code == 401
#         data = response.get_json()
#         assert data["error"] == "Invalid session data"


# class TestGetChildDashboardStats:       
#     @patch('src.routes.Session.query')
#     def test_missing_auth(self, mock_sess_query, client):
#         response = client.get('/child_dashboard_stats')
#         assert response.status_code == 403
#         data = response.get_json()
#         assert data["error"] == "Missing or malformed token"

#     @patch('src.routes.Session.query')
#     def test_invalid_token(self, mock_sess_query, client):
#         mock_sess_query.filter_by.return_value = SimpleNamespace(first=lambda: None)

#         response = client.get('/child_dashboard_stats', headers={
#             "Authorization": "Bearer invalid_token"
#         })

#         assert response.status_code == 401
#         data = response.get_json()
#         assert data["error"] == "Invalid or unauthorized session"

#     @patch('src.routes.Session.query')
#     def test_session_without_child_id(self, mock_sess_query, client):
#         session_mock = SimpleNamespace(
#             session_information={
#                 "email": "child@example.com"
#                 # No child_id
#             }
#         )
#         mock_sess_query.filter_by.return_value = SimpleNamespace(first=lambda: session_mock)

#         response = client.get('/child_dashboard_stats', headers={
#             "Authorization": "Bearer any_token"
#         })

#         assert response.status_code == 401
#         data = response.get_json()
#         assert data["error"] == "Invalid or unauthorized session"

#     @patch('src.routes.Session.query')
#     @patch('src.routes.LessonHistory.query')
#     @patch('src.routes.Lesson.query')
#     @patch('src.routes.BadgeHistory.query')
#     @patch('src.routes.Child.query')
#     def test_success_dashboard(self, mock_child_query, mock_badge_query, mock_lesson_query, mock_history_query, mock_sess_query, client):
#         session_mock = SimpleNamespace(
#             session_information={
#                 "child_id": 1,
#                 "email": "child@example.com"
#             }
#         )
#         mock_sess_query.filter_by.return_value = SimpleNamespace(first=lambda: session_mock)

#         # Mock lessons completed
#         mock_history_query.filter_by.return_value.count.return_value = 5

#         # Mock all lessons (say 2 lessons per 2 skills)
#         lesson1 = SimpleNamespace(lesson_id=1, skill_id=101)
#         lesson2 = SimpleNamespace(lesson_id=2, skill_id=101)
#         lesson3 = SimpleNamespace(lesson_id=3, skill_id=102)
#         lesson4 = SimpleNamespace(lesson_id=4, skill_id=102)
#         mock_lesson_query.all.return_value = [lesson1, lesson2, lesson3, lesson4]

#         # Mock skill completion: first skill fully completed, second skill not completed
#         mock_history_query.filter.return_value.count.side_effect = [2, 0]

#         # Mock badges
#         mock_badge_query.filter_by.return_value.count.return_value = 3

#         # Mock child streak
#         child_mock = SimpleNamespace(child_id=1, streak=7)
#         mock_child_query.get.return_value = child_mock

#         response = client.get('/child_dashboard_stats', headers={
#             "Authorization": "Bearer any_token"
#             })

#         assert response.status_code == 200
#         data = response.get_json()
#         assert data["lessons_completed"] == 5
#         assert data["skills_completed"] == 1
#         assert data["badges_earned"] == 3
#         assert data["streak"] == 7
#         assert data["leaderboard_rank"] == 1
#         assert isinstance(data["heatmap"], list)
#         assert data["heatmap"][0]["status"] == 1

#     @patch('src.routes.Session.query')
#     @patch('src.routes.LessonHistory.query')
#     @patch('src.routes.Lesson.query')
#     @patch('src.routes.BadgeHistory.query')
#     @patch('src.routes.Child.query')
#     def test_child_not_found(self, mock_child_query, mock_badge_query, mock_lesson_query, mock_history_query, mock_sess_query, client):
#         session_mock = SimpleNamespace(
#             session_information={
#                 "child_id": 99,
#                 "email": "child@example.com"
#             }
#         )
#         mock_sess_query.filter_by.return_value = SimpleNamespace(first=lambda: session_mock)

#         mock_history_query.filter_by.return_value.count.return_value = 0
#         mock_lesson_query.all.return_value = []
#         mock_history_query.filter.return_value.count.return_value = 0
#         mock_badge_query.filter_by.return_value.count.return_value = 0
#         mock_child_query.get.return_value = None  # child not found

#         response = client.get('/child_dashboard_stats', headers={
#             "Authorization": "Bearer any_token"
#         })

#         assert response.status_code == 200
#         data = response.get_json()
#         assert data["lessons_completed"] == 0
#         assert data["skills_completed"] == 0
#         assert data["badges_earned"] == 0
#         assert data["streak"] == 0

#     @patch('src.routes.Session.query')
#     @patch('src.routes.LessonHistory.query')
#     @patch('src.routes.Lesson.query')
#     @patch('src.routes.BadgeHistory.query')
#     @patch('src.routes.Child.query')
#     def test_dashboard_no_lessons_no_badges(self, mock_child_query, mock_badge_query, mock_lesson_query, mock_history_query, mock_sess_query, client):
#         session_mock = SimpleNamespace(
#             session_information={
#                 "child_id": 1,
#                 "email": "child@example.com"
#             }
#         )
#         mock_sess_query.filter_by.return_value = SimpleNamespace(first=lambda: session_mock)

#         mock_history_query.filter_by.return_value.count.return_value = 0
#         mock_lesson_query.all.return_value = []
#         mock_history_query.filter.return_value.count.return_value = 0
#         mock_badge_query.filter_by.return_value.count.return_value = 0
#         child_mock = SimpleNamespace(child_id=1, streak=0)
#         mock_child_query.get.return_value = child_mock

#         response = client.get('/child_dashboard_stats', headers={
#             "Authorization": "Bearer any_token"
#         })

#         assert response.status_code == 200
#         data = response.get_json()
#         assert data["lessons_completed"] == 0
#         assert data["skills_completed"] == 0
#         assert data["badges_earned"] == 0
#         assert data["streak"] == 0
        
        
# class TestGetUserSkillProgress:

#     @patch('src.routes.Session.query')
#     def test_missing_auth(self, mock_sess_query, client):
#         response = client.get('/skill_categories')
#         assert response.status_code == 403
#         data = response.get_json()
#         assert data["error"] == "Missing or malformed token"

#     @patch('src.routes.Session.query')
#     def test_invalid_token(self, mock_sess_query, client):
#         mock_sess_query.filter_by.return_value = SimpleNamespace(first=lambda: None)

#         response = client.get('/skill_categories', headers={
#             "Authorization": "Bearer invalid_token"
#         })

#         assert response.status_code == 401
#         data = response.get_json()
#         assert data["error"] == "Invalid or unauthorized session"

#     @patch('src.routes.Session.query')
#     def test_session_without_child_id(self, mock_sess_query, client):
#         session_mock = SimpleNamespace(
#             session_information={
#                 "email": "child@example.com"
#                 # No child_id
#             }
#         )
#         mock_sess_query.filter_by.return_value = SimpleNamespace(first=lambda: session_mock)

#         response = client.get('/skill_categories', headers={
#             "Authorization": "Bearer any_token"
#         })

#         assert response.status_code == 401
#         data = response.get_json()
#         assert data["error"] == "Invalid or unauthorized session"

#     @patch('src.routes.Session.query')
#     @patch('src.routes.LessonHistory.query')
#     @patch('src.routes.Lesson.query')
#     @patch('src.routes.Skill.query')
#     def test_success_skill_progress(self, mock_skill_query, mock_lesson_query, mock_history_query, mock_sess_query, client):
#         session_mock = SimpleNamespace(
#             session_information={
#                 "child_id": 1,
#                 "email": "child@example.com"
#             }
#         )
#         mock_sess_query.filter_by.return_value = SimpleNamespace(first=lambda: session_mock)

#         # Mock some skills
#         skill1 = SimpleNamespace(skill_id=101, name="Skill A")
#         skill2 = SimpleNamespace(skill_id=102, name="Skill B")
#         mock_skill_query.all.return_value = [skill1, skill2]

#         # Total lessons per skill
#         def total_lessons_side_effect(**kwargs):
#             if kwargs.get('skill_id') == 101:
#                 return SimpleNamespace(count=lambda: 5)
#             else:
#                 return SimpleNamespace(count=lambda: 3)
#         mock_lesson_query.filter_by.side_effect = total_lessons_side_effect

#         # Completed lessons per skill
#         mock_history_query.join.return_value.filter.return_value.count.side_effect = [3, 1]

#         response = client.get('/skill_categories', headers={
#             "Authorization": "Bearer any_token"
#         })

#         assert response.status_code == 200
#         data = response.get_json()
#         assert len(data) == 2

#         # Skill A → 3/5 → 60%
#         assert data[0]["name"] == "Skill A"
#         assert data[0]["percentage_completed"] == 60

#         # Skill B → 1/3 → 33%
#         assert data[1]["name"] == "Skill B"
#         assert data[1]["percentage_completed"] == 33

#     @patch('src.routes.Session.query')
#     @patch('src.routes.LessonHistory.query')
#     @patch('src.routes.Lesson.query')
#     @patch('src.routes.Skill.query')
#     def test_zero_lessons_edge_case(self, mock_skill_query, mock_lesson_query, mock_history_query, mock_sess_query, client):
#         session_mock = SimpleNamespace(
#             session_information={
#                 "child_id": 1,
#                 "email": "child@example.com"
#             }
#         )
#         mock_sess_query.filter_by.return_value = SimpleNamespace(first=lambda: session_mock)

#         # Skill with 0 lessons (edge case)
#         skill1 = SimpleNamespace(skill_id=201, name="Empty Skill")
#         mock_skill_query.all.return_value = [skill1]

#         mock_lesson_query.filter_by.return_value.count.return_value = 0
#         mock_history_query.join.return_value.filter.return_value.count.return_value = 0

#         response = client.get('/skill_categories', headers={
#             "Authorization": "Bearer any_token"
#         })

#         assert response.status_code == 200
#         data = response.get_json()
#         assert len(data) == 1
#         assert data[0]["name"] == "Empty Skill"
#         assert data[0]["percentage_completed"] == 0
        
        
# @api.route('/auth/parent_register', methods=['POST'])
# WILL UPDATE THIS SWAGGER SOON 
# def parent_register():
#     """
#     a new parent
#     ---
#     parameters:
#       - name: body
#         in: body
#         required: true
#         schema:
#           id: Parent
#           required:
#             - name
#             - email
#             - password
#           properties:
#             name:
#               type: string
#             email:
#               type: string
#             password:
#               type: string
#             profile_image:
#               type: string
#     responses:
#       201:
#         description: Created
#       409:
#         description: Conflict
#     """
#     ...
