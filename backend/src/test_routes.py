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

#  Test for CRUD of activities

def test_create_activity_success():
    tester = app.test_client()
    token = "607a510f-c2ef-4568-99dc-f7ed020c4139"  # Admin Token

    response = tester.post('/admin/activity',
        json={
            "title": "Test Activity",
            "description": "Do this",
            "image": "",
            "instructions": "Step 1, Step 2",
            "difficulty": "Easy",
            "answer_format": "text",
            "lesson_id": 1
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code in (201, 401)
 

def test_update_activity():
        tester = app.test_client()
        token = "607a510f-c2ef-4568-99dc-f7ed020c4139"
        response = tester.put('/admin/activity', json={
            "id": 1,
            "image": "",
            "title": "Updated Activity",
            "description": "Do this",
            "instructions": "Step 1, Step 2",
            "difficulty": "Easy",
            "lesson_id": 1 
        },
        headers={"Authorization": f"Bearer {token}"})
        assert response.status_code in (200, 401)
        data = response.get_json()
        assert "message" in data or "error" in data

def test_delete_activity():
    tester = app.test_client()
    token = "607a510f-c2ef-4568-99dc-f7ed020c4139"  
    response = tester.delete(
        '/admin/activity',
        json={"id": 1},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code in (200, 404)
    data = response.get_json()
    assert "message" in data or "error" in data



# Tests for lessons

def test_get_all_lessons():
    tester = app.test_client()
    token = "9f504415-5b14-4caf-839f-907f615dec38"
    response = tester.get('/lessons', headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

def test_create_lesson():
    tester = app.test_client()
    token = "74272d81-74fd-446d-910c-71162118a4ad"
    response = tester.post('/admin/lesson', json={
        "skill_id": 1,
        "title": "New Lesson",
        "content": {},
        "image": "",
        "description": "Intro to Something"
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code in (201, 400, 404)
    data = response.get_json()
    assert "id" in data or "error" in data

def test_update_lesson():
    tester = app.test_client()
    token = "74272d81-74fd-446d-910c-71162118a4ad"
    response = tester.put('/admin/lesson', json={
        "id": 1,
        "title": "Updated Lesson"
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code in (200, 404)
    data = response.get_json()
    assert "message" in data or "error" in data

def test_delete_lesson():
    tester = app.test_client()
    token = "74272d81-74fd-446d-910c-71162118a4ad"
    response = tester.delete('/admin/lesson', json={"id": 1},
                             headers={"Authorization": f"Bearer {token}"})
    assert response.status_code in (200, 404)
    data = response.get_json()
    assert "message" in data or "error" in data


#  QUIZ


def test_get_all_activities():
    tester = app.test_client()
    token = "9f504415-5b14-4caf-839f-907f615dec38"
    response = tester.get('/activities', headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)


def test_create_quiz():
    tester = app.test_client()
    token = "74272d81-74fd-446d-910c-71162118a4ad"
    response = tester.post('/admin/quiz', json={
        "title": "Test Quiz",
        "description": "Quiz Desc",
        "difficulty": "Easy",
        "points": 10,
        "lesson_id": 1,
        "time_duration": 60,
        "image": "",
        "questions": [{
            "question": "Sample Q?",
            "options": [
                {"text": "A", "isCorrect": False},
                {"text": "B", "isCorrect": True}
            ]
        }]
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code in (201, 400, 404)
    data = response.get_json()
    assert "id" in data or "error" in data

def test_update_quiz():
    tester = app.test_client()
    token = "74272d81-74fd-446d-910c-71162118a4ad"
    response = tester.put('/admin/quiz', json={
        "id": 1,
        "title": "Updated Quiz Title"
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code in (200, 404)
    data = response.get_json()
    assert "message" in data or "error" in data

def test_delete_quiz():
    tester = app.test_client()
    token = "74272d81-74fd-446d-910c-71162118a4ad"
    response = tester.delete('/admin/quiz', json={"id": 1},
                             headers={"Authorization": f"Bearer {token}"})
    assert response.status_code in (200, 404)
    data = response.get_json()
    assert "message" in data or "error" in data



def test_get_all_skills():
    tester = app.test_client()
    token = "9f504415-5b14-4caf-839f-907f615dec38"
    response = tester.get('/skills', headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)





# badges


def test_get_all_badges():
    tester = app.test_client()
    token = "9f504415-5b14-4caf-839f-907f615dec38"
    response = tester.get('/badges', headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

def test_create_badge():
    tester = app.test_client()
    token = "74272d81-74fd-446d-910c-71162118a4ad"
    response = tester.post('/admin/badge', json={
        "name": "Achievement Unlocked",
        "description": "Awarded for something",
        "image": ""
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code in (201, 400)
    data = response.get_json()
    assert "id" in data or "error" in data


def test_delete_badge():
    tester = app.test_client()
    token = "74272d81-74fd-446d-910c-71162118a4ad"
    response = tester.delete('/admin/badge', json={"id": 1},
                             headers={"Authorization": f"Bearer {token}"})
    assert response.status_code in (200, 404)
    data = response.get_json()
    assert "message" in data or "error" in data




# tests for parents

def test_get_all_parents():
    tester = app.test_client()
    token = "74272d81-74fd-446d-910c-71162118a4ad"   # admin token
    response = tester.get('/parents', headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    for parent in data:
        assert "id" in parent
        assert "name" in parent
        assert "email" in parent
        assert "blocked" in parent


def test_post_feedback_quiz():
    tester = app.test_client()
    token = "f84977fb-63e9-49f6-8bb6-125ddacd97c4"  #parent token

    response = tester.post('/feedback',
        headers={"Authorization": f"Bearer {token}"},
        json={
            "skill_type": "Quiz",
            "id": 1,  
            "text": "Very helpful quiz!"
        }
    )
    assert response.status_code in (200, 404) 
    data = response.get_json()
    assert "message" in data or "error" in data

def test_post_feedback_invalid_type():
    tester = app.test_client()
    token = "f84977fb-63e9-49f6-8bb6-125ddacd97c4"

    response = tester.post('/feedback',
        headers={"Authorization": f"Bearer {token}"},
        json={
            "skill_type": "InvalidType",
            "id": 1,
            "text": "Should fail"
        }
    )

    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
























