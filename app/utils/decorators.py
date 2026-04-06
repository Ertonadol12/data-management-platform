"""
Custom decorators for route protection and logging
"""

from functools import wraps
from flask import flash, redirect, url_for, session, request
from flask_login import current_user
from datetime import datetime

def login_required_ajax(f):
    """
    Decorator for AJAX endpoints that require login.
    Returns 401 instead of redirect for AJAX requests.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            from flask import jsonify
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """
    Decorator for admin-only routes.
    Currently checks if user is authenticated and has admin flag.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        
        # Check for admin role (you can add an is_admin field to User model)
        # For now, this is a placeholder
        if not hasattr(current_user, 'is_admin') or not current_user.is_admin:
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('main.dashboard'))
        
        return f(*args, **kwargs)
    return decorated_function

def log_activity(f):
    """
    Decorator to log user activity.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            # Log activity (you can implement this with a database table)
            print(f"[{datetime.now()}] User {current_user.username} accessed {request.path}")
        return f(*args, **kwargs)
    return decorated_function

def handle_errors(f):
    """
    Decorator to handle exceptions in routes.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            from flask import jsonify
            flash(f'An error occurred: {str(e)}', 'danger')
            return redirect(url_for('main.dashboard'))
    return decorated_function