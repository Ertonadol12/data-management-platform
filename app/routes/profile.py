"""
User Profile Routes
"""

from flask import render_template, jsonify, request, flash, redirect, url_for
from flask_login import login_required, current_user, logout_user
from app import db, bcrypt
from app.models.upload import Upload
from flask import Blueprint

bp = Blueprint('profile', __name__, url_prefix='/profile')

@bp.route('/')
@login_required
def profile_page():
    """User profile page"""
    return render_template('profile.html')

@bp.route('/api/profile', methods=['GET'])
@login_required
def api_get_profile():
    """Get user profile"""
    
    total_uploads = Upload.query.filter_by(user_id=current_user.id).count()
    total_size = db.session.query(db.func.sum(Upload.file_size)).filter_by(user_id=current_user.id).scalar() or 0
    
    return jsonify({
        'username': current_user.username,
        'email': current_user.email,
        'full_name': current_user.full_name,
        'member_since': current_user.created_at.strftime('%B %d, %Y'),
        'total_uploads': total_uploads,
        'total_storage_mb': round(total_size / (1024 * 1024), 2)
    })

@bp.route('/api/profile', methods=['PUT'])
@login_required
def api_update_profile():
    """Update user profile"""
    
    data = request.get_json()
    
    if 'full_name' in data:
        current_user.full_name = data['full_name']
    
    if 'email' in data:
        # Check if email is taken
        existing = User.query.filter_by(email=data['email']).first()
        if existing and existing.id != current_user.id:
            return jsonify({'success': False, 'message': 'Email already taken'}), 400
        current_user.email = data['email']
    
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Profile updated'})

@bp.route('/api/change-password', methods=['POST'])
@login_required
def api_change_password():
    """Change user password"""
    
    data = request.get_json()
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    
    if not bcrypt.check_password_hash(current_user.password_hash, current_password):
        return jsonify({'success': False, 'message': 'Current password is incorrect'}), 400
    
    if len(new_password) < 8:
        return jsonify({'success': False, 'message': 'Password must be at least 8 characters'}), 400
    
    current_user.password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Password changed successfully'})

@bp.route('/api/delete-account', methods=['DELETE'])
@login_required
def api_delete_account():
    """Delete user account"""
    
    # Delete all associated files (cascade will handle database)
    db.session.delete(current_user)
    db.session.commit()
    
    logout_user()
    
    return jsonify({'success': True, 'message': 'Account deleted'})