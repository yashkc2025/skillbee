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

# Authentication helper functions
class AuthHelper:
    """Helper class for handling authentication in tests"""
    
    def __init__(self, test_client):
        self.client = test_client
        self.tokens = {}
        self.created_sessions = []  # Track sessions for cleanup
        self.created_users = {      # Track created users for cleanup
            'children': [],
            'parents': [],
            'admins': []
        }
    
    def cleanup_sessions(self):
        """Clean up all sessions created during testing"""
        from .models import Session
        from .db import db
        
        with app.app_context():
            for token in self.created_sessions:
                session = Session.query.filter_by(session_id=token).first()
                if session:
                    db.session.delete(session)
            
            try:
                db.session.commit()
                self.created_sessions.clear()
                self.tokens.clear()
            except Exception as e:
                db.session.rollback()
                print(f"Session cleanup error: {e}")
    
    def cleanup_users(self):
        """Clean up all users created during testing"""
        from .models import Child, Parent, Admin
        from .db import db
        
        with app.app_context():
            try:
                # Clean up children
                for child_email in self.created_users['children']:
                    child = Child.query.filter_by(email_id=child_email).first()
                    if child:
                        db.session.delete(child)
                
                # Clean up parents  
                for parent_email in self.created_users['parents']:
                    parent = Parent.query.filter_by(email_id=parent_email).first()
                    if parent:
                        db.session.delete(parent)
                
                # Clean up admins (be careful with this)
                for admin_email in self.created_users['admins']:
                    admin = Admin.query.filter_by(email_id=admin_email).first()
                    if admin:
                        db.session.delete(admin)
                
                db.session.commit()
                self.created_users = {'children': [], 'parents': [], 'admins': []}
                print("User cleanup completed")
                
            except Exception as e:
                db.session.rollback()
                print(f"User cleanup error: {e}")
    
    def cleanup_all(self):
        """Clean up both sessions and users"""
        self.cleanup_sessions()
        self.cleanup_users()
    
    def login_child(self, email_or_username="testchild@gmail.com", password="abcdef"):
        """Login as a child and return the authentication token"""
        response = self.client.post('/auth/children_login', json={
            "email_or_username": email_or_username,
            "password": password
        })
        
        if response.status_code == 200:
            data = response.get_json()
            token = data['session']['token']
            self.tokens['child'] = token
            self.created_sessions.append(token)  # Track for cleanup
            return token
        return None
    
    def login_parent(self, email="testparent@example.com", password="1234"):
        """Login as a parent and return the authentication token"""
        response = self.client.post('/auth/parent_login', json={
            "email": email,
            "password": password
        })
        
        if response.status_code == 200:
            data = response.get_json()
            token = data['session']['token']
            self.tokens['parent'] = token
            self.created_sessions.append(token)  # Track for cleanup
            return token
        return None
    
    def login_admin(self, email_id="admin@gmail.com", password="1234"):
        """Login as admin and return the authentication token"""
        with app.app_context():
            admin_create()
            # Track admin creation for cleanup (be careful with this)
            if email_id not in self.created_users['admins']:
                self.created_users['admins'].append(email_id)
        
        response = self.client.post('/auth/admin_login', json={
            "email_id": email_id,
            "password": password
        })
        
        if response.status_code in (200, 201):
            data = response.get_json()
            token = data['session']['token']
            self.tokens['admin'] = token
            self.created_sessions.append(token)  # Track for cleanup
            return token
        return None
    
    def get_auth_headers(self, role):
        """Get authorization headers for a specific role"""
        token = self.tokens.get(role)
        if token:
            return {'Authorization': f'Bearer {token}'}
        return {}
    
    def register_child(self, name="test child", email="testchild@gmail.com", 
                      username="ubbbbbbb", password="abcdef", 
                      dob="2014-09-09", school="abcd"):
        """Register a test child account"""
        with app.app_context():
            response = self.client.post('/auth/children_register', json={
                "name": name,
                "email": email,
                "password": password,
                "username": username,
                "dob": dob,
                "school": school,
                "profile_image": ""
            })
            
            # Track successful registrations for cleanup
            if response.status_code in (201, 409):  # Created or already exists
                if email not in self.created_users['children']:
                    self.created_users['children'].append(email)
            
            return response
    
    def register_parent(self, name="Test Parent", email="testparent@example.com", 
                       password="1234"):
        """Register a test parent account"""
        response = self.client.post('/auth/parent_register', json={
            "name": name,
            "email": email,
            "password": password,
            "profile_image": ""
        })
        
        # Track successful registrations for cleanup
        if response.status_code in (201, 409):  # Created or already exists
            if email not in self.created_users['parents']:
                self.created_users['parents'].append(email)
        
        return response


def cleanup_test_user(email, user_type):
    """Clean up a specific test user and all related data"""
    from .models import Child, Parent, Session
    from .db import db
    
    with app.app_context():
        try:
            if user_type == 'child':
                # Find and delete the child user
                child = Child.query.filter_by(email_id=email).first()
                if child:
                    # Delete all sessions for this child
                    sessions = Session.query.all()
                    for session in sessions:
                        session_info = session.session_information
                        if 'child_id' in session_info and session_info['child_id'] == child.child_id:
                            db.session.delete(session)
                    
                    # Delete the child
                    db.session.delete(child)
                    
            elif user_type == 'parent':
                # Find and delete the parent user
                parent = Parent.query.filter_by(email_id=email).first()
                if parent:
                    # Delete all sessions for this parent
                    sessions = Session.query.all()
                    for session in sessions:
                        session_info = session.session_information
                        if 'parent_id' in session_info and session_info['parent_id'] == parent.parent_id:
                            db.session.delete(session)
                    
                    # Delete the parent
                    db.session.delete(parent)
            
            db.session.commit()
            print(f"Cleaned up {user_type} user: {email}")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error cleaning up {user_type} user {email}: {e}")


@pytest.fixture
def auth_helper():
    """Pytest fixture to provide authentication helper with automatic cleanup"""
    tester = app.test_client()
    helper = AuthHelper(tester)
    
    yield helper  # Provide the helper to the test
    
    # Cleanup after test completes
    helper.cleanup_all()

@pytest.fixture
def authenticated_child():
    """Pytest fixture that provides an authenticated child session"""
    tester = app.test_client()
    auth = AuthHelper(tester)
    
    # Register child if needed
    auth.register_child()
    
    # Login and get token
    token = auth.login_child()
    
    result = {
        'client': tester,
        'auth': auth,
        'token': token,
        'headers': auth.get_auth_headers('child')
    }
    
    yield result  # Provide to test
    
    # Cleanup after test
    auth.cleanup_all()

@pytest.fixture
def authenticated_parent():
    """Pytest fixture that provides an authenticated parent session"""
    tester = app.test_client()
    auth = AuthHelper(tester)
    
    # Register parent if needed
    auth.register_parent()
    
    # Login and get token
    token = auth.login_parent()
    
    result = {
        'client': tester,
        'auth': auth,
        'token': token,
        'headers': auth.get_auth_headers('parent')
    }
    
    yield result  # Provide to test
    
    # Cleanup after test
    auth.cleanup_all()

@pytest.fixture
def authenticated_admin():
    """Pytest fixture that provides an authenticated admin session"""
    tester = app.test_client()
    auth = AuthHelper(tester)
    
    # Login as admin
    token = auth.login_admin()
    
    result = {
        'client': tester,
        'auth': auth,
        'token': token,
        'headers': auth.get_auth_headers('admin')
    }
    
    yield result  # Provide to test
    
    # Cleanup after test
    auth.cleanup_all()

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
        auth = AuthHelper(tester)
        
        # Create a test child user
        test_email = "login_test@gmail.com"
        test_username = "logintest"
        test_password = "testpass123"
        
        try:
            # Register the child
            auth.register_child(
                name="Login Test Child",
                email=test_email,
                username=test_username,
                password=test_password,
                dob="2014-05-15",
                school="Test School"
            )
            
            # Test login
            response = tester.post('/auth/children_login', json={
                "email_or_username": test_email,
                "password": test_password
            })
            assert response.status_code == 200
            data = response.get_json()
            assert "user" in data
            assert "session" in data
            assert "token" in data["session"]
            
        finally:
            # Clean up: Delete the test child and all related data
            cleanup_test_user(test_email, 'child')
    
    
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
























# Testing functions for child API endpoints

def test_child_curriculums_success(authenticated_child):
    """Test successful retrieval of curriculums for authenticated child"""
    client = authenticated_child['client']
    auth = authenticated_child['auth']
    
    # Create a test child user
    test_email = "curriculums_test@gmail.com"
    test_username = "curriculumstest"
    test_password = "testpass123"
    
    try:
        # Register the child
        auth.register_child(
            name="Curriculums Test Child",
            email=test_email,
            username=test_username,
            password=test_password,
            dob="2014-05-15",
            school="Test School"
        )
        
        # Login with the test child
        token = auth.login_child(test_email, test_password)
        headers = {'Authorization': f'Bearer {token}'} if token else {}
    
        response = client.get('/api/child/curriculums', headers=headers)
        
        assert response.status_code == 200
        data = response.get_json()
        
        # Verify response structure
        assert "curriculums" in data
        assert isinstance(data["curriculums"], list)
        
        # If curriculums exist, verify structure
        if data["curriculums"]:
            curriculum = data["curriculums"][0]
            assert "curriculum_id" in curriculum
            assert "name" in curriculum
            assert "description" in curriculum
            assert "image" in curriculum
            assert "progress_status" in curriculum
            
    finally:
        # Clean up: Delete the test child and all related data
        cleanup_test_user(test_email, 'child')
        
        # Verify data types
        assert isinstance(curriculum["curriculum_id"], int)
        assert isinstance(curriculum["name"], str)
        assert isinstance(curriculum["progress_status"], int)
        assert 0 <= curriculum["progress_status"] <= 100


def test_child_curriculums_failures():
    """Test all failure cases for child curriculums endpoint"""
    tester = app.test_client()
    
    # Test 1: Missing authentication token
    response = tester.get('/api/child/curriculums')
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Token is missing"
    
    # Test 2: Invalid authentication token
    response = tester.get('/api/child/curriculums', headers={
        'Authorization': 'Bearer invalid_token_here'
    })
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Invalid token"
    
    # Test 3: Expired token (we can't easily test this without manipulating time)
    # This would be handled by the token_required decorator
    
    # Test 4: Wrong role - try with parent token if available
    # First register and login as parent
    tester.post('/auth/parent_register', json={
        "name": "Test Parent",
        "email": "testparent_curriculum@example.com",
        "password": "1234",
        "profile_image": ""
    })
    
    parent_login_response = tester.post('/auth/parent_login', json={
        "email": "testparent_curriculum@example.com",
        "password": "1234"
    })
    
    if parent_login_response.status_code == 200:
        parent_data = parent_login_response.get_json()
        parent_token = parent_data['session']['token']
        
        response = tester.get('/api/child/curriculums', headers={
            'Authorization': f'Bearer {parent_token}'
        })
        assert response.status_code == 403
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Insufficient permissions"
    
    # Test 5: Malformed Authorization header
    response = tester.get('/api/child/curriculums', headers={
        'Authorization': 'InvalidFormat'
    })
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Invalid token"  # Malformed header gets treated as invalid token
    
    # Test 6: Empty Authorization header
    response = tester.get('/api/child/curriculums', headers={
        'Authorization': ''
    })
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Token is missing"


def test_child_curriculum_lessons_success(authenticated_child):
    """Test successful retrieval of lessons for a specific curriculum for authenticated child"""
    client = authenticated_child['client']
    auth = authenticated_child['auth']
    
    # Create a test child user
    test_email = "curriculum_lessons_test@gmail.com"
    test_username = "curriculumlessonstest"
    test_password = "testpass123"
    
    try:
        # Register the child
        auth.register_child(
            name="Curriculum Lessons Test Child",
            email=test_email,
            username=test_username,
            password=test_password,
            dob="2014-05-15",
            school="Test School"
        )
        
        # Login with the test child
        token = auth.login_child(test_email, test_password)
        headers = {'Authorization': f'Bearer {token}'} if token else {}
    
        # Test with curriculum_id = 1 (assuming it exists in test data)
        curriculum_id = 1
        response = client.get(f'/api/child/curriculum/{curriculum_id}/lessons', headers=headers)
        
        # Should return 200 even if no lessons found (returns error in JSON)
        assert response.status_code in [200, 404]
        data = response.get_json()
        
        if response.status_code == 200:
            # Verify response structure for successful case
            assert "curriculum" in data
            assert "lessons" in data
            
            # Verify curriculum structure
            curriculum = data["curriculum"]
            assert "curriculum_id" in curriculum
            assert "name" in curriculum
            assert isinstance(curriculum["curriculum_id"], int)
            assert isinstance(curriculum["name"], str)
            
            # Verify lessons structure
            assert isinstance(data["lessons"], list)
            
            # If lessons exist, verify structure
            if data["lessons"]:
                lesson = data["lessons"][0]
                assert "lesson_id" in lesson
                assert "title" in lesson
                assert "image" in lesson
                assert "description" in lesson
                assert "progress_status" in lesson
                
                # Verify data types
                assert isinstance(lesson["lesson_id"], int)
                assert isinstance(lesson["title"], str)
                assert isinstance(lesson["progress_status"], (int, float))
                assert 0 <= lesson["progress_status"] <= 100
        
        elif response.status_code == 404:
            # Verify error structure for skill not found
            assert "error" in data
            assert data["error"] in ["Skill not found", "No lessons found for this skill"]
            
    finally:
        # Clean up: Delete the test child and all related data
        cleanup_test_user(test_email, 'child')


def test_child_curriculum_lessons_failures():
    """Test all failure cases for child curriculum lessons endpoint"""
    tester = app.test_client()
    
    # Test 1: Missing authentication token
    response = tester.get('/api/child/curriculum/1/lessons')
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Token is missing"
    
    # Test 2: Invalid authentication token
    response = tester.get('/api/child/curriculum/1/lessons', headers={
        'Authorization': 'Bearer invalid_token_here'
    })
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Invalid token"
    
    # Test 3: Wrong role - try with parent token
    # First register and login as parent
    tester.post('/auth/parent_register', json={
        "name": "Test Parent",
        "email": "testparent_lessons@example.com",
        "password": "1234",
        "profile_image": ""
    })
    
    parent_login_response = tester.post('/auth/parent_login', json={
        "email": "testparent_lessons@example.com",
        "password": "1234"
    })
    
    if parent_login_response.status_code == 200:
        parent_data = parent_login_response.get_json()
        parent_token = parent_data['session']['token']
        
        response = tester.get('/api/child/curriculum/1/lessons', headers={
            'Authorization': f'Bearer {parent_token}'
        })
        assert response.status_code == 403
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Insufficient permissions"
    
    # Test 4: Valid auth but non-existent curriculum ID
    # Register and login as child for this test
    tester.post('/auth/children_register', json={
        "name": "test child lessons",
        "email": "testchild_lessons@gmail.com",
        "password": "abcdef",
        "username": "testchild_lessons",
        "dob": "2014-09-09",
        "school": "abcd",
        "profile_image": ""
    })
    
    child_login_response = tester.post('/auth/children_login', json={
        "email_or_username": "testchild_lessons@gmail.com",
        "password": "abcdef"
    })
    
    if child_login_response.status_code == 200:
        child_data = child_login_response.get_json()
        child_token = child_data['session']['token']
        
        # Test with very large curriculum_id that shouldn't exist
        response = tester.get('/api/child/curriculum/99999/lessons', headers={
            'Authorization': f'Bearer {child_token}'
        })
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Skill not found"
    
    # Test 5: Invalid curriculum_id format (non-integer)
    # This would be handled by Flask's URL routing, resulting in 404
    response = tester.get('/api/child/curriculum/invalid/lessons', headers={
        'Authorization': 'Bearer some_token'
    })
    assert response.status_code == 404  # Flask routing error
    
    # Test 6: Negative curriculum_id
    if child_login_response.status_code == 200:
        response = tester.get('/api/child/curriculum/-1/lessons', headers={
            'Authorization': f'Bearer {child_token}'
        })
        assert response.status_code == 404
        data = response.get_json()
        # Handle case where Flask might return None for invalid routes
        if data is not None:
            assert "error" in data
            assert data["error"] == "Skill not found"
    
    # Test 7: Malformed Authorization header
    response = tester.get('/api/child/curriculum/1/lessons', headers={
        'Authorization': 'InvalidFormat'
    })
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Invalid token"
    
    # Test 8: Empty Authorization header
    response = tester.get('/api/child/curriculum/1/lessons', headers={
        'Authorization': ''
    })
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Token is missing"


def test_child_lesson_details_success(authenticated_child):
    """Test successful retrieval of lesson details for authenticated child"""
    client = authenticated_child['client']
    auth = authenticated_child['auth']
    
    # Create a test child user
    test_email = "lesson_details_test@gmail.com"
    test_username = "lessondetailstest"
    test_password = "testpass123"
    
    try:
        # Register the child
        auth.register_child(
            name="Lesson Details Test Child",
            email=test_email,
            username=test_username,
            password=test_password,
            dob="2014-05-15",
            school="Test School"
        )
        
        # Login with the test child
        token = auth.login_child(test_email, test_password)
        headers = {'Authorization': f'Bearer {token}'} if token else {}
    
        # Test with lesson_id = 1 (assuming it exists in test data)
        lesson_id = 1
        response = client.get(f'/api/child/lesson/{lesson_id}', headers=headers)
        
        # Should return 200 for valid lesson or 404 for non-existent lesson
        assert response.status_code in [200, 404]
        data = response.get_json()
        
        if response.status_code == 200:
            # Verify response structure for successful case
            assert "lesson_id" in data
            assert "title" in data
            assert "content" in data
            assert "image" in data
            assert "completed_at" in data
            
            # Verify data types
            assert isinstance(data["lesson_id"], int)
            assert isinstance(data["title"], str)
            assert isinstance(data["content"], str)
            # image can be None or binary data
            # completed_at can be None or ISO datetime string
            if data["completed_at"] is not None:
                assert isinstance(data["completed_at"], str)
        
        elif response.status_code == 404:
            # Verify error structure for lesson not found
            assert "error" in data
            assert data["error"] == "Lesson not found"
            
    finally:
        # Clean up: Delete the test child and all related data
        cleanup_test_user(test_email, 'child')


def test_child_lesson_details_failures():
    """Test all failure cases for child lesson details endpoint"""
    tester = app.test_client()
    
    # Test 1: Missing authentication token
    response = tester.get('/api/child/lesson/1')
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Token is missing"
    
    # Test 2: Invalid authentication token
    response = tester.get('/api/child/lesson/1', headers={
        'Authorization': 'Bearer invalid_token_here'
    })
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Invalid token"
    
    # Test 3: Wrong role - try with parent token
    # First register and login as parent
    tester.post('/auth/parent_register', json={
        "name": "Test Parent",
        "email": "testparent_lesson@example.com",
        "password": "1234",
        "profile_image": ""
    })
    
    parent_login_response = tester.post('/auth/parent_login', json={
        "email": "testparent_lesson@example.com",
        "password": "1234"
    })
    
    if parent_login_response.status_code == 200:
        parent_data = parent_login_response.get_json()
        parent_token = parent_data['session']['token']
        
        response = tester.get('/api/child/lesson/1', headers={
            'Authorization': f'Bearer {parent_token}'
        })
        assert response.status_code == 403
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Insufficient permissions"
    
    # Test 4: Valid auth but non-existent lesson ID
    # Register and login as child for this test
    tester.post('/auth/children_register', json={
        "name": "test child lesson",
        "email": "testchild_lesson@gmail.com",
        "password": "abcdef",
        "username": "testchild_lesson",
        "dob": "2014-09-09",
        "school": "abcd",
        "profile_image": ""
    })
    
    child_login_response = tester.post('/auth/children_login', json={
        "email_or_username": "testchild_lesson@gmail.com",
        "password": "abcdef"
    })
    
    if child_login_response.status_code == 200:
        child_data = child_login_response.get_json()
        child_token = child_data['session']['token']
        
        # Test with very large lesson_id that shouldn't exist
        response = tester.get('/api/child/lesson/99999', headers={
            'Authorization': f'Bearer {child_token}'
        })
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Lesson not found"
    
    # Test 5: Invalid lesson_id format (non-integer)
    # This would be handled by Flask's URL routing, resulting in 404
    response = tester.get('/api/child/lesson/invalid', headers={
        'Authorization': 'Bearer some_token'
    })
    assert response.status_code == 404  # Flask routing error
    
    # Test 6: Negative lesson_id
    if child_login_response.status_code == 200:
        response = tester.get('/api/child/lesson/-1', headers={
            'Authorization': f'Bearer {child_token}'
        })
        assert response.status_code == 404
        data = response.get_json()
        # Handle case where Flask might return None for invalid routes
        if data is not None:
            assert "error" in data
            assert data["error"] == "Lesson not found"
    
    # Test 7: Zero lesson_id
    if child_login_response.status_code == 200:
        response = tester.get('/api/child/lesson/0', headers={
            'Authorization': f'Bearer {child_token}'
        })
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Lesson not found"
    
    # Test 8: Malformed Authorization header
    response = tester.get('/api/child/lesson/1', headers={
        'Authorization': 'InvalidFormat'
    })
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Invalid token"
    
    # Test 9: Empty Authorization header
    response = tester.get('/api/child/lesson/1', headers={
        'Authorization': ''
    })
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Token is missing"


def test_child_lesson_mark_read_success(authenticated_child):
    """Test successful marking of lesson as completed for authenticated child"""
    client = authenticated_child['client']
    auth = authenticated_child['auth']
    
    # Create a test child user
    test_email = "lesson_mark_read_test@gmail.com"
    test_username = "lessonmarkreadtest"
    test_password = "testpass123"
    
    try:
        # Register the child
        auth.register_child(
            name="Lesson Mark Read Test Child",
            email=test_email,
            username=test_username,
            password=test_password,
            dob="2014-05-15",
            school="Test School"
        )
        
        # Login with the test child
        token = auth.login_child(test_email, test_password)
        headers = {'Authorization': f'Bearer {token}'} if token else {}
    
        # Test with lesson_id = 1 (assuming it exists in test data)
        lesson_id = 1
        
        # Test without providing completed_at (should use current time)
        response = client.post(f'/api/child/lesson/{lesson_id}/mark-read', 
                              headers=headers, 
                              json={})  # Empty JSON body
        
        # Should return 201 for successful completion, 200 if already completed, or 404 for non-existent lesson
        assert response.status_code in [200, 201, 404]
        data = response.get_json()
        
        if response.status_code == 201:
            # Verify response structure for successful case
            assert "message" in data
            assert data["message"] == "Lesson marked as completed"
            
            # Test marking the same lesson again (should return 200 with different message)
            response2 = client.post(f'/api/child/lesson/{lesson_id}/mark-read', 
                                   headers=headers, 
                                   json={})
            assert response2.status_code == 200
            data2 = response2.get_json()
            assert "message" in data2
            assert data2["message"] == "Lesson already completed"
        
        elif response.status_code == 200:
            # Lesson was already completed from previous test run
            assert "message" in data
            assert data["message"] == "Lesson already completed"
        
        elif response.status_code == 404:
            # Verify error structure for lesson not found
            assert "error" in data
            assert data["error"] == "Lesson not found"
        
        # Test with custom completed_at timestamp
        lesson_id_2 = 2
        custom_timestamp = "2024-01-15T10:30:00Z"
        response3 = client.post(f'/api/child/lesson/{lesson_id_2}/mark-read', 
                               headers=headers,
                               json={"completed_at": custom_timestamp})
        
        # Should handle custom timestamp properly
        assert response3.status_code in [200, 201, 404, 400]  # 400 for invalid date format, 200 if already completed
        data3 = response3.get_json()
        
        if response3.status_code == 201:
            assert data3["message"] == "Lesson marked as completed"
        elif response3.status_code == 200:
            assert data3["message"] == "Lesson already completed"
        elif response3.status_code == 404:
            assert data3["error"] == "Lesson not found"
            
    finally:
        # Clean up: Delete the test child and all related data
        cleanup_test_user(test_email, 'child')


def test_child_lesson_mark_read_failures():
    """Test all failure cases for child lesson mark-read endpoint"""
    tester = app.test_client()
    
    # Test 1: Missing authentication token
    response = tester.post('/api/child/lesson/1/mark-read', json={})
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Token is missing"
    
    # Test 2: Invalid authentication token
    response = tester.post('/api/child/lesson/1/mark-read', 
                          headers={'Authorization': 'Bearer invalid_token_here'},
                          json={})
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Invalid token"
    
    # Test 3: Wrong role - try with parent token
    # First register and login as parent
    tester.post('/auth/parent_register', json={
        "name": "Test Parent",
        "email": "testparent_markread@example.com",
        "password": "1234",
        "profile_image": ""
    })
    
    parent_login_response = tester.post('/auth/parent_login', json={
        "email": "testparent_markread@example.com",
        "password": "1234"
    })
    
    if parent_login_response.status_code == 200:
        parent_data = parent_login_response.get_json()
        parent_token = parent_data['session']['token']
        
        response = tester.post('/api/child/lesson/1/mark-read', 
                              headers={'Authorization': f'Bearer {parent_token}'},
                              json={})
        assert response.status_code == 403
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Insufficient permissions"
    
    # Test 4: Valid auth but non-existent lesson ID
    # Register and login as child for this test
    tester.post('/auth/children_register', json={
        "name": "test child markread",
        "email": "testchild_markread@gmail.com",
        "password": "abcdef",
        "username": "testchild_markread",
        "dob": "2014-09-09",
        "school": "abcd",
        "profile_image": ""
    })
    
    child_login_response = tester.post('/auth/children_login', json={
        "email_or_username": "testchild_markread@gmail.com",
        "password": "abcdef"
    })
    
    if child_login_response.status_code == 200:
        child_data = child_login_response.get_json()
        child_token = child_data['session']['token']
        
        # Test with very large lesson_id that shouldn't exist
        response = tester.post('/api/child/lesson/99999/mark-read', 
                              headers={'Authorization': f'Bearer {child_token}'},
                              json={})
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Lesson not found"
    
    # Test 5: Invalid lesson_id format (non-integer)
    # This would be handled by Flask's URL routing, resulting in 404
    response = tester.post('/api/child/lesson/invalid/mark-read', 
                          headers={'Authorization': 'Bearer some_token'},
                          json={})
    assert response.status_code == 404  # Flask routing error
    
    # Test 6: Invalid date format in request body
    if child_login_response.status_code == 200:
        response = tester.post('/api/child/lesson/1/mark-read', 
                              headers={'Authorization': f'Bearer {child_token}'},
                              json={"completed_at": "invalid-date-format"})
        # Should return 400 for invalid date format, 404 if lesson doesn't exist, or 200 if already completed
        assert response.status_code in [400, 404, 200]
        data = response.get_json()
        assert "error" in data or "message" in data
        if response.status_code == 400:
            assert data["error"] == "Invalid date format"
        elif response.status_code == 404:
            assert data["error"] == "Lesson not found"
        elif response.status_code == 200:
            assert data["message"] == "Lesson already completed"
    
    # Test 7: Negative lesson_id
    if child_login_response.status_code == 200:
        response = tester.post('/api/child/lesson/-1/mark-read', 
                              headers={'Authorization': f'Bearer {child_token}'},
                              json={})
        assert response.status_code == 404
        data = response.get_json()
        # Handle case where Flask might return None for invalid routes
        if data is not None:
            assert "error" in data
            assert data["error"] == "Lesson not found"
    
    # Test 8: Zero lesson_id
    if child_login_response.status_code == 200:
        response = tester.post('/api/child/lesson/0/mark-read', 
                              headers={'Authorization': f'Bearer {child_token}'},
                              json={})
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Lesson not found"
    
    # Test 9: Malformed Authorization header
    response = tester.post('/api/child/lesson/1/mark-read', 
                          headers={'Authorization': 'InvalidFormat'},
                          json={})
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Invalid token"
    
    # Test 10: Empty Authorization header
    response = tester.post('/api/child/lesson/1/mark-read', 
                          headers={'Authorization': ''},
                          json={})
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Token is missing"
    
    # Test 11: Invalid JSON payload structure
    if child_login_response.status_code == 200:
        response = tester.post('/api/child/lesson/1/mark-read', 
                              headers={'Authorization': f'Bearer {child_token}'},
                              json={"invalid_field": "some_value"})
        # Should still work as completed_at is optional
        assert response.status_code in [201, 404, 200]  # 200 if already completed
        data = response.get_json()
        assert "message" in data or "error" in data


def test_child_lesson_activities_success(authenticated_child):
    """Test successful retrieval of lesson activities"""
    client = authenticated_child['client']
    auth = authenticated_child['auth']
    
    # Create a test child user
    test_email = "lesson_activities_test@gmail.com"
    test_username = "lessonactivitiestest"
    test_password = "testpass123"
    
    try:
        # Register the child
        auth.register_child(
            name="Lesson Activities Test Child",
            email=test_email,
            username=test_username,
            password=test_password,
            dob="2014-05-15",
            school="Test School"
        )
        
        # Login with the test child
        token = auth.login_child(test_email, test_password)
        headers = {'Authorization': f'Bearer {token}'} if token else {}
    
        # Test successful retrieval of activities for lesson 1
        response = client.get('/api/child/lesson/1/activities', headers=headers)
        
        # Should return 200 with activities data structure
        assert response.status_code == 200
        data = response.get_json()
        
        # Verify response structure
        assert 'curriculum' in data
        assert 'lesson' in data 
        assert 'activities' in data
        
        # Verify curriculum structure
        curriculum = data['curriculum']
        assert 'curriculum_id' in curriculum
        assert 'name' in curriculum
        
        # Verify lesson structure
        lesson = data['lesson']
        assert 'lesson_id' in lesson
        assert 'title' in lesson
        assert lesson['lesson_id'] == 1
        
        # Verify activities structure
        activities = data['activities']
        assert isinstance(activities, list)
        
        # If activities exist, verify structure
        if activities:
            activity = activities[0]
            assert 'activity_id' in activity
            assert 'name' in activity
            assert 'description' in activity
            assert 'image' in activity
            assert 'progress_status' in activity
            assert activity['progress_status'] in [0, 100]
            
    finally:
        # Clean up: Delete the test child and all related data
        cleanup_test_user(test_email, 'child')


def test_child_lesson_activities_failures():
    """Test various failure scenarios for lesson activities endpoint"""
    tester = app.test_client()
    auth_helper = AuthHelper(tester)
    
    # Test 1: No authorization header
    response = tester.get('/api/child/lesson/1/activities')
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Token is missing"
    
    # Test 2: Invalid token
    response = tester.get('/api/child/lesson/1/activities',
                         headers={'Authorization': 'Bearer invalid_token'})
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Invalid token"
    
    # Login as child for role-based tests
    child_login_response = tester.post('/auth/children_login', json={
        "email": "john.doe@example.com",
        "password": "password"
    })
    
    child_token = None
    if child_login_response.status_code == 200:
        child_data = child_login_response.get_json()
        child_token = child_data["token"]
        auth_helper.created_sessions.append(child_token)
    
    # Login as parent for unauthorized role test
    parent_login_response = tester.post('/auth/parent_login', json={
        "email": "jane.doe@example.com", 
        "password": "password"
    })
    
    parent_token = None
    if parent_login_response.status_code == 200:
        parent_data = parent_login_response.get_json()
        parent_token = parent_data["token"]
        auth_helper.created_sessions.append(parent_token)
    
    # Test 3: Parent role accessing child endpoint (forbidden)
    if parent_token:
        response = tester.get('/api/child/lesson/1/activities',
                             headers={'Authorization': f'Bearer {parent_token}'})
        assert response.status_code == 403
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Insufficient permissions"
    
    # Test 4: Invalid lesson ID (non-existent)
    if child_token:
        response = tester.get('/api/child/lesson/99999/activities',
                             headers={'Authorization': f'Bearer {child_token}'})
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Lesson not found"
    
    # Test 5: Zero lesson_id
    if child_token:
        response = tester.get('/api/child/lesson/0/activities',
                             headers={'Authorization': f'Bearer {child_token}'})
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Lesson not found"
    
    # Test 6: Negative lesson_id
    if child_token:
        response = tester.get('/api/child/lesson/-1/activities',
                             headers={'Authorization': f'Bearer {child_token}'})
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data
    
    # Test 7: Malformed Authorization header
    response = tester.get('/api/child/lesson/1/activities',
                         headers={'Authorization': 'InvalidFormat'})
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Invalid token"
    
    # Test 8: Empty Authorization header
    response = tester.get('/api/child/lesson/1/activities',
                         headers={'Authorization': ''})
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Token is missing"
    
    # Cleanup
    auth_helper.cleanup_sessions()


def test_child_activity_details_success(authenticated_child):
    """Test successful retrieval of activity details"""
    client = authenticated_child['client']
    auth = authenticated_child['auth']
    
    # Create a test child user
    test_email = "activity_details_test@gmail.com"
    test_username = "activitydetailstest"
    test_password = "testpass123"
    
    try:
        # Register the child
        auth.register_child(
            name="Activity Details Test Child",
            email=test_email,
            username=test_username,
            password=test_password,
            dob="2014-05-15",
            school="Test School"
        )
        
        # Login with the test child
        token = auth.login_child(test_email, test_password)
        headers = {'Authorization': f'Bearer {token}'} if token else {}
    
        # Test successful retrieval of activity details for activity 1
        response = client.get('/api/child/activity/1', headers=headers)
        
        # Should return 200 with activity data or 404 if activity doesn't exist for this child
        assert response.status_code in [200, 404]
        
        if response.status_code == 200:
            data = response.get_json()
            
            # Verify response structure for successful retrieval
            assert 'activity_id' in data
            assert 'name' in data
            assert 'description' in data
            assert 'image' in data
            assert 'answer_format' in data
            assert 'completed_at' in data  # Can be None if not completed
            
            # Verify activity_id matches requested ID
            assert data['activity_id'] == 1
            
            # Verify data types
            assert isinstance(data['activity_id'], int)
            assert isinstance(data['name'], str)
            assert isinstance(data['description'], str)
            assert isinstance(data['answer_format'], str)
            
            # completed_at can be None or a string (ISO format)
            if data['completed_at'] is not None:
                assert isinstance(data['completed_at'], str)
        
        elif response.status_code == 404:
            data = response.get_json()
            assert 'error' in data
            assert data['error'] == 'Activity not found'
            
    finally:
        # Clean up: Delete the test child and all related data
        cleanup_test_user(test_email, 'child')


def test_child_activity_details_failures():
    """Test various failure scenarios for activity details endpoint"""
    tester = app.test_client()
    auth_helper = AuthHelper(tester)
    
    # Test 1: No authorization header
    response = tester.get('/api/child/activity/1')
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Token is missing"
    
    # Test 2: Invalid token
    response = tester.get('/api/child/activity/1',
                         headers={'Authorization': 'Bearer invalid_token'})
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Invalid token"
    
    # Login as child for role-based tests
    child_login_response = tester.post('/auth/children_login', json={
        "email": "john.doe@example.com",
        "password": "password"
    })
    
    child_token = None
    if child_login_response.status_code == 200:
        child_data = child_login_response.get_json()
        child_token = child_data["token"]
        auth_helper.created_sessions.append(child_token)
    
    # Login as parent for unauthorized role test
    parent_login_response = tester.post('/auth/parent_login', json={
        "email": "jane.doe@example.com", 
        "password": "password"
    })
    
    parent_token = None
    if parent_login_response.status_code == 200:
        parent_data = parent_login_response.get_json()
        parent_token = parent_data["token"]
        auth_helper.created_sessions.append(parent_token)
    
    # Test 3: Parent role accessing child endpoint (forbidden)
    if parent_token:
        response = tester.get('/api/child/activity/1',
                             headers={'Authorization': f'Bearer {parent_token}'})
        assert response.status_code == 403
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Insufficient permissions"
    
    # Test 4: Invalid activity ID (non-existent)
    if child_token:
        response = tester.get('/api/child/activity/99999',
                             headers={'Authorization': f'Bearer {child_token}'})
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Activity not found"
    
    # Test 5: Zero activity_id
    if child_token:
        response = tester.get('/api/child/activity/0',
                             headers={'Authorization': f'Bearer {child_token}'})
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Activity not found"
    
    # Test 6: Negative activity_id
    if child_token:
        response = tester.get('/api/child/activity/-1',
                             headers={'Authorization': f'Bearer {child_token}'})
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Activity not found"
    
    # Test 7: Malformed Authorization header
    response = tester.get('/api/child/activity/1',
                         headers={'Authorization': 'InvalidFormat'})
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Invalid token"
    
    # Test 8: Empty Authorization header
    response = tester.get('/api/child/activity/1',
                         headers={'Authorization': ''})
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Token is missing"
    
    # Test 9: Activity belonging to different child (should return 404)
    # This tests the child_id filter in the query
    if child_token:
        # Attempt to access an activity that might exist but doesn't belong to this child
        response = tester.get('/api/child/activity/1000',
                             headers={'Authorization': f'Bearer {child_token}'})
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Activity not found"
    
    # Cleanup
    auth_helper.cleanup_sessions()


def test_child_activity_submit_failures():
    """Test various failure scenarios for activity submission endpoint"""
    tester = app.test_client()
    auth_helper = AuthHelper(tester)
    
    # Test file content for uploads
    test_file_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde'
    
    # Test 1: No authorization header
    from io import BytesIO
    response = tester.post('/api/child/activity/1/submit',
                          data={'file': (BytesIO(test_file_content), 'test.png')},
                          content_type='multipart/form-data')
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Token is missing"
    
    # Test 2: Invalid token
    response = tester.post('/api/child/activity/1/submit',
                          headers={'Authorization': 'Bearer invalid_token'},
                          data={'file': (BytesIO(test_file_content), 'test.png')},
                          content_type='multipart/form-data')
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Invalid token"
    
    # Login as child for role-based tests
    child_login_response = tester.post('/auth/children_login', json={
        "email": "john.doe@example.com",
        "password": "password"
    })
    
    child_token = None
    if child_login_response.status_code == 200:
        child_data = child_login_response.get_json()
        child_token = child_data["token"]
        auth_helper.created_sessions.append(child_token)
    
    # Login as parent for unauthorized role test
    parent_login_response = tester.post('/auth/parent_login', json={
        "email": "jane.doe@example.com", 
        "password": "password"
    })
    
    parent_token = None
    if parent_login_response.status_code == 200:
        parent_data = parent_login_response.get_json()
        parent_token = parent_data["token"]
        auth_helper.created_sessions.append(parent_token)
    
    # Test 3: Parent role accessing child endpoint (forbidden)
    if parent_token:
        response = tester.post('/api/child/activity/1/submit',
                              headers={'Authorization': f'Bearer {parent_token}'},
                              data={'file': (BytesIO(test_file_content), 'test.png')},
                              content_type='multipart/form-data')
        assert response.status_code == 403
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Insufficient permissions"
    
    # Test 4: Invalid activity ID (non-existent)
    if child_token:
        response = tester.post('/api/child/activity/99999/submit',
                              headers={'Authorization': f'Bearer {child_token}'},
                              data={'file': (BytesIO(test_file_content), 'test.png')},
                              content_type='multipart/form-data')
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Activity not found"
    
    # Test 5: No file uploaded
    if child_token:
        response = tester.post('/api/child/activity/1/submit',
                              headers={'Authorization': f'Bearer {child_token}'},
                              data={})
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "No file uploaded or unsupported content type"
    
    # Test 6: Empty file
    if child_token:
        response = tester.post('/api/child/activity/1/submit',
                              headers={'Authorization': f'Bearer {child_token}'},
                              data={'file': (BytesIO(b''), '')},
                              content_type='multipart/form-data')
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "No file selected"
    
    # Test 7: Invalid file format
    if child_token:
        invalid_file_content = b'invalid file content'
        response = tester.post('/api/child/activity/1/submit',
                              headers={'Authorization': f'Bearer {child_token}'},
                              data={'file': (BytesIO(invalid_file_content), 'test.txt')},
                              content_type='multipart/form-data')
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Invalid file format. Only JPG, JPEG, PNG, or PDF allowed"
    
    # Test 8: File too large (simulate by checking content length if possible)
    if child_token:
        # Create a large file content (over 10MB simulated)
        large_file_content = b'x' * (11 * 1024 * 1024)  # 11MB
        response = tester.post('/api/child/activity/1/submit',
                              headers={'Authorization': f'Bearer {child_token}'},
                              data={'file': (BytesIO(large_file_content), 'large.png')},
                              content_type='multipart/form-data')
        # Should return 400 for file too large or 413 Request Entity Too Large
        assert response.status_code in [400, 413]
        if response.status_code == 400:
            data = response.get_json()
            assert "error" in data
            # Check for file size error
            assert "size" in data["error"].lower() or "large" in data["error"].lower()
    
    # Test 9: Unsupported content type
    if child_token:
        response = tester.post('/api/child/activity/1/submit',
                              headers={'Authorization': f'Bearer {child_token}', 'Content-Type': 'text/plain'},
                              data=b'plain text data')
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "No file uploaded or unsupported content type"
    
    # Test 10: Zero activity_id
    if child_token:
        response = tester.post('/api/child/activity/0/submit',
                              headers={'Authorization': f'Bearer {child_token}'},
                              data={'file': (BytesIO(test_file_content), 'test.png')},
                              content_type='multipart/form-data')
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Activity not found"
    
    # Test 11: Malformed Authorization header
    response = tester.post('/api/child/activity/1/submit',
                          headers={'Authorization': 'InvalidFormat'},
                          data={'file': (BytesIO(test_file_content), 'test.png')},
                          content_type='multipart/form-data')
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Invalid token"
    
    # Cleanup
    auth_helper.cleanup_sessions()


def test_child_activity_history_failures():
    """Test various failure scenarios for activity history endpoint"""
    tester = app.test_client()
    auth_helper = AuthHelper(tester)
    
    # Test 1: No authorization header
    response = tester.get('/api/child/activity/1/history')
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Token is missing"
    
    # Test 2: Invalid token
    response = tester.get('/api/child/activity/1/history',
                         headers={'Authorization': 'Bearer invalid_token'})
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Invalid token"
    
    # Login as child for role-based tests
    child_login_response = tester.post('/auth/children_login', json={
        "email": "john.doe@example.com",
        "password": "password"
    })
    
    child_token = None
    if child_login_response.status_code == 200:
        child_data = child_login_response.get_json()
        child_token = child_data["token"]
        auth_helper.created_sessions.append(child_token)
    
    # Login as parent for unauthorized role test
    parent_login_response = tester.post('/auth/parent_login', json={
        "email": "jane.doe@example.com", 
        "password": "password"
    })
    
    parent_token = None
    if parent_login_response.status_code == 200:
        parent_data = parent_login_response.get_json()
        parent_token = parent_data["token"]
        auth_helper.created_sessions.append(parent_token)
    
    # Test 3: Parent role accessing child endpoint (forbidden)
    if parent_token:
        response = tester.get('/api/child/activity/1/history',
                             headers={'Authorization': f'Bearer {parent_token}'})
        assert response.status_code == 403
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Insufficient permissions"
    
    # Test 4: Invalid activity ID (non-existent)
    if child_token:
        response = tester.get('/api/child/activity/99999/history',
                             headers={'Authorization': f'Bearer {child_token}'})
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Activity not found"
    
    # Test 5: Zero activity_id
    if child_token:
        response = tester.get('/api/child/activity/0/history',
                             headers={'Authorization': f'Bearer {child_token}'})
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Activity not found"
    
    # Test 6: Negative activity_id
    if child_token:
        response = tester.get('/api/child/activity/-1/history',
                             headers={'Authorization': f'Bearer {child_token}'})
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Activity not found"
    
    # Test 7: Activity belonging to different child (should return 404)
    # This tests the child_id filter in the query
    if child_token:
        response = tester.get('/api/child/activity/1000/history',
                             headers={'Authorization': f'Bearer {child_token}'})
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Activity not found"
    
    # Test 8: Malformed Authorization header
    response = tester.get('/api/child/activity/1/history',
                         headers={'Authorization': 'InvalidFormat'})
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Invalid token"
    
    # Test 9: Empty Authorization header
    response = tester.get('/api/child/activity/1/history',
                         headers={'Authorization': ''})
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Token is missing"
    
    # Test 10: Expired token (simulated by invalid token format)
    response = tester.get('/api/child/activity/1/history',
                         headers={'Authorization': 'Bearer expired_token_12345'})
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Invalid token"
    
    # Cleanup
    auth_helper.cleanup_sessions()


def test_child_activity_submission_download_failures():
    """Test various failure scenarios for activity submission download endpoint"""
    tester = app.test_client()
    auth_helper = AuthHelper(tester)
    
    # Test 1: No authorization header
    response = tester.get('/api/child/activity/history/1')
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Token is missing"
    
    # Test 2: Invalid token
    response = tester.get('/api/child/activity/history/1',
                         headers={'Authorization': 'Bearer invalid_token'})
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Invalid token"
    
    # Login as child for role-based tests
    child_login_response = tester.post('/auth/children_login', json={
        "email": "john.doe@example.com",
        "password": "password"
    })
    
    child_token = None
    if child_login_response.status_code == 200:
        child_data = child_login_response.get_json()
        child_token = child_data["token"]
        auth_helper.created_sessions.append(child_token)
    
    # Login as parent for unauthorized role test
    parent_login_response = tester.post('/auth/parent_login', json={
        "email": "jane.doe@example.com", 
        "password": "password"
    })
    
    parent_token = None
    if parent_login_response.status_code == 200:
        parent_data = parent_login_response.get_json()
        parent_token = parent_data["token"]
        auth_helper.created_sessions.append(parent_token)
    
    # Test 3: Parent role accessing child endpoint (forbidden)
    if parent_token:
        response = tester.get('/api/child/activity/history/1',
                             headers={'Authorization': f'Bearer {parent_token}'})
        assert response.status_code == 403
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Insufficient permissions"
    
    # Test 4: Invalid activity_history_id (non-existent)
    if child_token:
        response = tester.get('/api/child/activity/history/99999',
                             headers={'Authorization': f'Bearer {child_token}'})
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Submission not found"
    
    # Test 5: Zero activity_history_id
    if child_token:
        response = tester.get('/api/child/activity/history/0',
                             headers={'Authorization': f'Bearer {child_token}'})
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Submission not found"
    
    # Test 6: Negative activity_history_id
    if child_token:
        response = tester.get('/api/child/activity/history/-1',
                             headers={'Authorization': f'Bearer {child_token}'})
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Submission not found"
    
    # Test 7: Submission belonging to different child's activity (access control)
    if child_token:
        # Try to access a submission that might exist but belongs to different child
        response = tester.get('/api/child/activity/history/1000',
                             headers={'Authorization': f'Bearer {child_token}'})
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data
        assert data["error"] in [
            "Submission not found",
            "Associated activity not found"
        ]
    
    # Test 8: Malformed Authorization header
    response = tester.get('/api/child/activity/history/1',
                         headers={'Authorization': 'InvalidFormat'})
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Invalid token"
    
    # Test 9: Empty Authorization header
    response = tester.get('/api/child/activity/history/1',
                         headers={'Authorization': ''})
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Token is missing"
    
    # Test 10: Invalid token format (Bearer missing)
    response = tester.get('/api/child/activity/history/1',
                         headers={'Authorization': 'invalid_token_format'})
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Invalid token"
    
    # Test 11: Expired token simulation
    if child_token:
        response = tester.get('/api/child/activity/history/1',
                             headers={'Authorization': 'Bearer expired_token_simulation'})
        assert response.status_code == 401
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Invalid token"
    
    # Cleanup
    auth_helper.cleanup_sessions()


def test_child_lesson_quizzes_success(authenticated_child):
    """Test successful retrieval of lesson quizzes"""
    client = authenticated_child['client']
    auth = authenticated_child['auth']
    
    # Create a test child user
    test_email = "lesson_quizzes_test@gmail.com"
    test_username = "lessonquizzestest"
    test_password = "testpass123"
    
    try:
        # Register the child
        auth.register_child(
            name="Lesson Quizzes Test Child",
            email=test_email,
            username=test_username,
            password=test_password,
            dob="2014-05-15",
            school="Test School"
        )
        
        # Login with the test child
        token = auth.login_child(test_email, test_password)
        headers = {'Authorization': f'Bearer {token}'} if token else {}
    
        # Test successful retrieval of quizzes for lesson 1
        response = client.get('/api/child/lesson/1/quizzes', headers=headers)
        
        # Should return 200 with quizzes data or 404 if lesson doesn't exist
        assert response.status_code in [200, 404]
        
        if response.status_code == 200:
            data = response.get_json()
            
            # Verify response structure
            assert 'curriculum' in data
            assert 'lesson' in data 
            assert 'quizzes' in data
            
            # Verify curriculum structure
            curriculum = data['curriculum']
            assert 'curriculum_id' in curriculum
            assert 'name' in curriculum
            assert isinstance(curriculum['curriculum_id'], int)
            assert isinstance(curriculum['name'], str)
            
            # Verify lesson structure
            lesson = data['lesson']
            assert 'lesson_id' in lesson
            assert 'title' in lesson
            assert lesson['lesson_id'] == 1
            assert isinstance(lesson['lesson_id'], int)
            assert isinstance(lesson['title'], str)
            
            # Verify quizzes structure
            quizzes = data['quizzes']
            assert isinstance(quizzes, list)
            
            # If quizzes exist, verify structure
            if quizzes:
                quiz = quizzes[0]
                
                # Verify quiz structure
                assert 'quiz_id' in quiz
                assert 'name' in quiz
                assert 'description' in quiz
                assert 'time_duration' in quiz
                assert 'progress_status' in quiz
                assert 'image' in quiz
                
                # Verify data types
                assert isinstance(quiz['quiz_id'], int)
                assert isinstance(quiz['name'], str)
                assert isinstance(quiz['description'], str)
                assert isinstance(quiz['time_duration'], int)
                assert isinstance(quiz['progress_status'], int)
                
                # Verify progress_status is either 0 or 100
                assert quiz['progress_status'] in [0, 100]
                
                # image can be string or None
                if quiz['image'] is not None:
                    assert isinstance(quiz['image'], str)
        
        elif response.status_code == 404:
            data = response.get_json()
            assert 'error' in data
            assert data['error'] in [
                'Lesson not found or does not belong to the curriculum',
                'Curriculum not found'
            ]
            
    finally:
        # Clean up: Delete the test child and all related data
        cleanup_test_user(test_email, 'child')


def test_child_lesson_quizzes_failures():
    """Test various failure scenarios for lesson quizzes endpoint"""
    tester = app.test_client()
    auth_helper = AuthHelper(tester)
    
    # Test 1: No authorization header
    response = tester.get('/api/child/lesson/1/quizzes')
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Token is missing"
    
    # Test 2: Invalid token
    response = tester.get('/api/child/lesson/1/quizzes',
                         headers={'Authorization': 'Bearer invalid_token'})
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Invalid token"
    
    # Login as child for role-based tests
    child_login_response = tester.post('/auth/children_login', json={
        "email": "john.doe@example.com",
        "password": "password"
    })
    
    child_token = None
    if child_login_response.status_code == 200:
        child_data = child_login_response.get_json()
        child_token = child_data["token"]
        auth_helper.created_sessions.append(child_token)
    
    # Login as parent for unauthorized role test
    parent_login_response = tester.post('/auth/parent_login', json={
        "email": "jane.doe@example.com", 
        "password": "password"
    })
    
    parent_token = None
    if parent_login_response.status_code == 200:
        parent_data = parent_login_response.get_json()
        parent_token = parent_data["token"]
        auth_helper.created_sessions.append(parent_token)
    
    # Test 3: Parent role accessing child endpoint (forbidden)
    if parent_token:
        response = tester.get('/api/child/lesson/1/quizzes',
                             headers={'Authorization': f'Bearer {parent_token}'})
        assert response.status_code == 403
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Insufficient permissions"
    
    # Test 4: Invalid lesson ID (non-existent)
    if child_token:
        response = tester.get('/api/child/lesson/99999/quizzes',
                             headers={'Authorization': f'Bearer {child_token}'})
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Lesson not found or does not belong to the curriculum"
    
    # Test 5: Zero lesson_id
    if child_token:
        response = tester.get('/api/child/lesson/0/quizzes',
                             headers={'Authorization': f'Bearer {child_token}'})
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Lesson not found or does not belong to the curriculum"
    
    # Test 6: Negative lesson_id
    if child_token:
        response = tester.get('/api/child/lesson/-1/quizzes',
                             headers={'Authorization': f'Bearer {child_token}'})
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Lesson not found or does not belong to the curriculum"
    
    # Test 7: Lesson that doesn't exist in the curriculum
    if child_token:
        response = tester.get('/api/child/lesson/1000/quizzes',
                             headers={'Authorization': f'Bearer {child_token}'})
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Lesson not found or does not belong to the curriculum"
    
    # Test 8: Malformed Authorization header
    response = tester.get('/api/child/lesson/1/quizzes',
                         headers={'Authorization': 'InvalidFormat'})
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Invalid token"
    
    # Test 9: Empty Authorization header
    response = tester.get('/api/child/lesson/1/quizzes',
                         headers={'Authorization': ''})
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Token is missing"
    
    # Test 10: Missing Bearer prefix
    response = tester.get('/api/child/lesson/1/quizzes',
                         headers={'Authorization': 'invalid_token_without_bearer'})
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Invalid token"
    
    # Test 11: Expired token simulation
    response = tester.get('/api/child/lesson/1/quizzes',
                         headers={'Authorization': 'Bearer expired_token_simulation'})
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Invalid token"
    
    # Cleanup
    auth_helper.cleanup_sessions()


def test_child_quiz_questions_success(authenticated_child):
    """Test successful retrieval of quiz questions"""
    client = authenticated_child['client']
    auth = authenticated_child['auth']
    
    # Create a test child user
    test_email = "quiz_questions_test@gmail.com"
    test_username = "quizquestionstest"
    test_password = "testpass123"
    
    try:
        # Register the child
        auth.register_child(
            name="Quiz Questions Test Child",
            email=test_email,
            username=test_username,
            password=test_password,
            dob="2014-05-15",
            school="Test School"
        )
        
        # Login with the test child
        token = auth.login_child(test_email, test_password)
        headers = {'Authorization': f'Bearer {token}'} if token else {}
    
        # Test 1: Get quiz questions for curriculum 1, lesson 1, quiz 1
        response = client.get('/api/child/curriculum/1/lesson/1/quiz/1',
                             headers=headers)
        
        # Should return 200 with quiz questions data or 404 if curriculum/lesson/quiz doesn't exist
        assert response.status_code in [200, 404]
        
        if response.status_code == 200:
            data = response.get_json()
            
            # Verify response structure
            assert "curriculum" in data
            assert "lesson" in data
            assert "quiz" in data
            assert "questions" in data
            
            # Verify curriculum data
            assert "curriculum_id" in data["curriculum"]
            assert "curriculum_name" in data["curriculum"]
            
            # Verify lesson data
            assert "lesson_id" in data["lesson"]
            assert "lesson_name" in data["lesson"]
            
            # Verify quiz data
            assert "quiz_id" in data["quiz"]
            assert "quiz_name" in data["quiz"]
            
            # Verify questions structure
            assert isinstance(data["questions"], list)
            if data["questions"]:  # If questions exist
                question = data["questions"][0]
                assert "question_index" in question
                assert "question" in question
                assert "options" in question
                assert "marks" in question
                assert isinstance(question["options"], list)
                
    finally:
        # Clean up: Delete the test child and all related data
        cleanup_test_user(test_email, 'child')


def test_child_settings_success(authenticated_child):
    """Test successful retrieval of child profile/settings"""
    client = authenticated_child['client']
    auth = authenticated_child['auth']
    
    # Create a test child user
    test_email = "child_settings_test@gmail.com"
    test_username = "childsettingstest"
    test_password = "testpass123"
    
    try:
        # Register the child
        auth.register_child(
            name="Child Settings Test Child",
            email=test_email,
            username=test_username,
            password=test_password,
            dob="2014-05-15",
            school="Test School"
        )
        
        # Login with the test child
        token = auth.login_child(test_email, test_password)
        headers = {'Authorization': f'Bearer {token}'} if token else {}
    
        # Test 1: Get child profile/settings
        response = client.get('/api/child/setting',
                             headers=headers)
        
        # Should return 200 with profile data
        assert response.status_code == 200
        
        data = response.get_json()
        
        # Verify response structure
        assert "profile_image_url" in data
        assert "name" in data
        assert "dob" in data
        assert "email" in data
        assert "school" in data
        
        # Verify data types
        assert isinstance(data["profile_image_url"], str)
        assert isinstance(data["name"], str)
        # dob can be None or ISO date string
        assert data["dob"] is None or isinstance(data["dob"], str)
        assert isinstance(data["email"], str)
        assert isinstance(data["school"], str)
        
        # Verify name and email are not empty
        assert len(data["name"]) > 0
        assert len(data["email"]) > 0
        
        # If dob is provided, verify it's a valid ISO format
        if data["dob"]:
            from datetime import datetime
            try:
                datetime.fromisoformat(data["dob"])
            except ValueError:
                assert False, "Invalid date format in dob field"
                
    finally:
        # Clean up: Delete the test child and all related data
        cleanup_test_user(test_email, 'child')


def test_child_settings_failures(authenticated_child):
    """Test various failure scenarios for child settings endpoint"""
    client = authenticated_child['client']
    headers = authenticated_child['headers']
    
    # Test 1: Missing Authorization header
    response = client.get('/api/child/setting')
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Token is missing"
    
    # Test 2: Invalid token
    response = client.get('/api/child/setting',
                         headers={'Authorization': 'Bearer invalid_token'})
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Invalid token"
    
    # Test 3: Malformed Authorization header
    response = client.get('/api/child/setting',
                         headers={'Authorization': 'InvalidFormat'})
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Invalid token"
    
    # Test 4: Empty Authorization header
    response = client.get('/api/child/setting',
                         headers={'Authorization': ''})
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Token is missing"
    
    # Test 5: Missing Bearer prefix
    response = client.get('/api/child/setting',
                         headers={'Authorization': 'invalid_token_without_bearer'})
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Invalid token"
    
    # Test 6: Expired token simulation
    response = client.get('/api/child/setting',
                         headers={'Authorization': 'Bearer expired_token_simulation'})
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Invalid token"
    
    # Test 7: Wrong role token (simulate admin/parent token)
    # Note: This would require creating a different type of user, but the endpoint
    # is already protected by @token_required(allowed_roles=['child'])
    # so any non-child token would be rejected
    
    # Test 8: Invalid HTTP method (testing with POST instead of GET)
    response = client.post('/api/child/setting',
                          headers=headers,
                          json={"test": "data"})
    assert response.status_code == 405  # Method Not Allowed


def test_child_update_profile_failures(authenticated_child):
    """Test various failure scenarios for child profile update endpoint"""
    client = authenticated_child['client']
    auth = authenticated_child['auth']
    
    # Create a test child user
    test_email = "profile_fail_test@gmail.com"
    test_username = "profilefailtest"
    test_password = "testpass123"
    
    # Register the child
    auth.register_child(
        name="Profile Fail Test Child",
        email=test_email,
        username=test_username,
        password=test_password,
        dob="2014-05-15",
        school="Test School"
    )
    
    # Login with the test child
    token = auth.login_child(test_email, test_password)
    headers = {'Authorization': f'Bearer {token}'} if token else {}
    
    try:
        # Test 1: No data provided (Flask returns 415 for missing content-type)
        response = client.put('/api/child/update_profile',
                             headers=headers)
        assert response.status_code == 415
        # Note: When no JSON data/content-type is provided, Flask returns 415
        
        # Test 2: Empty JSON data
        response = client.put('/api/child/update_profile',
                             headers=headers,
                             json={})
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "No data provided"  # This is what the controller actually returns
        
        # Test 3: Invalid fields only
        response = client.put('/api/child/update_profile',
                             headers=headers,
                             json={"invalid_field": "value"})
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "At least one field must be provided"
        
        # Test 4: Empty name
        response = client.put('/api/child/update_profile',
                             headers=headers,
                             json={"name": ""})
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Name cannot be empty"
        
        # Test 5: Name with only whitespace
        response = client.put('/api/child/update_profile',
                             headers=headers,
                             json={"name": "   "})
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Name cannot be empty"
        
        # Test 6: Invalid date format
        response = client.put('/api/child/update_profile',
                             headers=headers,
                             json={"dob": "invalid-date"})
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Invalid date format. Use YYYY-MM-DD"
        
        # Test 7: Age too young (under 8 years)
        from datetime import date, timedelta
        too_young_dob = date.today() - timedelta(days=5*365)  # 5 years old
        response = client.put('/api/child/update_profile',
                             headers=headers,
                             json={"dob": too_young_dob.strftime('%Y-%m-%d')})
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Child must be between 8 and 14 years old"
        
        # Test 8: Age too old (over 14 years)
        too_old_dob = date.today() - timedelta(days=16*365)  # 16 years old
        response = client.put('/api/child/update_profile',
                             headers=headers,
                             json={"dob": too_old_dob.strftime('%Y-%m-%d')})
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Child must be between 8 and 14 years old"
        
        # Test 9: Empty date of birth
        response = client.put('/api/child/update_profile',
                             headers=headers,
                             json={"dob": ""})
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Date of birth cannot be empty"
        
        # Test 10: Missing Authorization header
        response = client.put('/api/child/update_profile',
                             json={"name": "Test Name"})
        assert response.status_code == 401
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Token is missing"
        
        # Test 11: Invalid token
        response = client.put('/api/child/update_profile',
                             headers={'Authorization': 'Bearer invalid_token'},
                             json={"name": "Test Name"})
        assert response.status_code == 401
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Invalid token"
        
        # Test 12: Malformed Authorization header
        response = client.put('/api/child/update_profile',
                             headers={'Authorization': 'InvalidFormat'},
                             json={"name": "Test Name"})
        assert response.status_code == 401
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Invalid token"
        
        # Test 13: Empty Authorization header
        response = client.put('/api/child/update_profile',
                             headers={'Authorization': ''},
                             json={"name": "Test Name"})
        assert response.status_code == 401
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Token is missing"
        
        # Test 14: Missing Bearer prefix
        response = client.put('/api/child/update_profile',
                             headers={'Authorization': 'invalid_token_without_bearer'},
                             json={"name": "Test Name"})
        assert response.status_code == 401
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Invalid token"
        
        # Test 15: Expired token simulation
        response = client.put('/api/child/update_profile',
                             headers={'Authorization': 'Bearer expired_token_simulation'},
                             json={"name": "Test Name"})
        assert response.status_code == 401
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Invalid token"
        
        # Test 2: No data provided
        response = client.put('/api/child/update_profile',
                             headers=headers,
                             json={})
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "No data provided"
        
    finally:
        # Clean up: Delete the test child and all related data
        cleanup_test_user(test_email, 'child')


# Database cleanup utilities for testing
def cleanup_test_data():
    """Clean up test data from database tables"""
    from .models import Session, Parent, Child, Admin
    from .db import db
    
    with app.app_context():
        try:
            # Delete test sessions
            Session.query.delete()
            
            # Delete test users (use pattern matching to be safer)
            # Delete children with test emails
            Child.query.filter(
                Child.email_id.like('%test%') | 
                Child.email_id.in_(['testchild@gmail.com'])
            ).delete(synchronize_session=False)
            
            # Delete parents with test emails  
            Parent.query.filter(
                Parent.email_id.like('%test%') |
                Parent.email_id.in_(['testparent@example.com'])
            ).delete(synchronize_session=False)
            
            # Be very careful with admin deletion - only delete test admins
            # Admin.query.filter(Admin.email_id == 'admin@gmail.com').delete()
            
            db.session.commit()
            print("Test data cleanup completed")
        except Exception as e:
            db.session.rollback()
            print(f"Cleanup error: {e}")

def cleanup_all_test_data():
    """More aggressive cleanup - use with caution"""
    from .models import Session, Parent, Child, LessonHistory, ActivityHistory, QuizHistory, BadgeHistory, Activity
    from .db import db
    
    with app.app_context():
        try:
            # Clean up all test-related data
            Session.query.delete()
            
            # Get test user IDs first
            test_children = Child.query.filter(
                Child.email_id.like('%test%') | 
                Child.email_id.in_(['testchild@gmail.com'])
            ).all()
            
            test_parents = Parent.query.filter(
                Parent.email_id.like('%test%') |
                Parent.email_id.in_(['testparent@example.com'])  
            ).all()
            
            # Clean up child-related history records
            for child in test_children:
                LessonHistory.query.filter_by(child_id=child.child_id).delete()
                # For ActivityHistory, we need to join with Activity to filter by child_id
                ActivityHistory.query.join(Activity).filter(Activity.child_id == child.child_id).delete(synchronize_session=False)
                QuizHistory.query.filter_by(child_id=child.child_id).delete()
                BadgeHistory.query.filter_by(child_id=child.child_id).delete()
            
            # Delete test users
            for child in test_children:
                db.session.delete(child)
                
            for parent in test_parents:
                db.session.delete(parent)
            
            db.session.commit()
            print("Comprehensive test data cleanup completed")
            
        except Exception as e:
            db.session.rollback()
            print(f"Comprehensive cleanup error: {e}")
            db.session.rollback()
            print(f"Comprehensive cleanup error: {e}")

@pytest.fixture(scope="session", autouse=True)
def cleanup_after_all_tests():
    """Automatically clean up after all tests complete"""
    yield  # Run all tests first
    cleanup_all_test_data()  # Then comprehensive cleanup







