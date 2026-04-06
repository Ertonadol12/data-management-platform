"""
History Routes
"""

from flask import render_template, jsonify, request
from flask_login import login_required, current_user
from app import db
from app.models.upload import Upload
from flask import Blueprint

bp = Blueprint('history', __name__, url_prefix='/history')

@bp.route('/')
@login_required
def history_page():
    """Upload history page"""
    return render_template('history.html')

@bp.route('/api/history')
@login_required
def api_history():
    """API endpoint for upload history"""
    
    search = request.args.get('search', '')
    status = request.args.get('status', '')
    page = int(request.args.get('page', 1))
    per_page = 10
    
    query = Upload.query.filter_by(user_id=current_user.id)
    
    if search:
        query = query.filter(Upload.original_filename.contains(search))
    
    if status:
        query = query.filter_by(status=status)
    
    paginated = query.order_by(Upload.uploaded_at.desc()).paginate(page=page, per_page=per_page)
    
    uploads = []
    for upload in paginated.items:
        uploads.append({
            'id': upload.id,
            'filename': upload.original_filename,
            'file_type': upload.file_type,
            'file_size': upload.file_size,
            'row_count': upload.row_count,
            'status': upload.status,
            'uploaded_at': upload.uploaded_at.strftime('%Y-%m-%d %H:%M')
        })
    
    return jsonify({
        'uploads': uploads,
        'total': paginated.total,
        'page': page,
        'pages': paginated.pages
    })