"""
Main Routes - Dashboard and Home
"""

from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models.upload import Upload
from flask import Blueprint
from sqlalchemy import func

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Redirect to dashboard if logged in, else login"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))

@bp.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard page"""
    
    # Statistics
    total_uploads = Upload.query.filter_by(user_id=current_user.id).count()
    processed_uploads = Upload.query.filter_by(user_id=current_user.id, status='completed').count()
    
    success_rate = (processed_uploads / total_uploads * 100) if total_uploads > 0 else 0
    
    # Recent uploads
    recent_uploads = Upload.query.filter_by(user_id=current_user.id).order_by(Upload.uploaded_at.desc()).limit(5).all()
    
    return render_template('dashboard.html',
                         total_uploads=total_uploads,
                         processed_uploads=processed_uploads,
                         success_rate=round(success_rate, 1),
                         recent_uploads=recent_uploads)