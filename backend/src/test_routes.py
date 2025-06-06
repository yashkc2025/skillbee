import json
from flask import Flask
from .routes import api
from flasgger import Swagger
from . import create_app
# Swagger(api)
app=create_app()

def test_parent_register_success():
    # to test the registration function of parent success
    tester = app.test_client()
    response = tester.post('/auth/parent_register', json={
        "name": "Test Parent",
        "email_id": "testparent@example.com",
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
        "email_id": "", 
        "password": "1234",
        "profile_image": ""
    })
    assert response.status_code in (400, 404)
    data = response.get_json()
    assert "error" in data

def test_children_register_success():
    # to test the registration function of child success
    tester = app.test_client()
    response = tester.post('/auth/children_register', json={
    "name":"test child",
    "email_id": "testchild@gmail.com",
    "password": "abcdef",
    "username": "ubbbbbbb",
    "dob": "2009-09-09",
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
    "email_id": "",
    "password": "",
    "username": "ubbbbbbb",
    "dob": "2009-09-09",
    "school": "sphs",
    "profile_image": ""
})
    assert response.status_code in (400, 404)
    data = response.get_json()
    assert "error" in data







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
