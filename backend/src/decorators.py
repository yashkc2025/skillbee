from functools import wraps
from flask import request, jsonify
from .models import Session, Child, Parent, Admin

def get_session_info():
    """Utility function to extract and validate session token."""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return None, jsonify({'error': 'Missing or malformed token'}), 403

    token = auth_header.split(" ")[1]
    session = Session.query.filter_by(session_id=token).first()
    if not session:
        return None, jsonify({'error': 'Invalid credentials'}), 401

    return session.session_information, None, None

def only_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session_info, error_response, status_code = get_session_info()
        if error_response:
            return error_response, status_code
        
        if "admin_id" not in session_info:
            return jsonify({'error': 'Forbidden — Admins only'}), 403

        return f(session_info, *args, **kwargs)
    return decorated_function

def only_parent(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session_info, error_response, status_code = get_session_info()
        if error_response:
            return error_response, status_code
        
        if "parent_id" not in session_info:
            return jsonify({'error': 'Forbidden — Parents only'}), 403

        return f(session_info, *args, **kwargs)
    return decorated_function

def only_admin_or_parent(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session_info, error_response, status_code = get_session_info()
        if error_response:
            return error_response, status_code
        
        if "admin_id" not in session_info and "parent_id" not in session_info:
            return jsonify({'error': 'Forbidden — Admin or Parent only'}), 403

        return f(session_info, *args, **kwargs)
    return decorated_function
