"""
File Upload Routes
"""

import os
import pandas as pd
from flask import render_template, request, jsonify, session, url_for, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models.upload import Upload
from app.models.processed import ProcessedFile
from app.services.file_handler import save_uploaded_file, get_file_info
from flask import Blueprint
from datetime import datetime
import json
import traceback

bp = Blueprint('upload', __name__, url_prefix='/upload')

ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls', 'json'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/')
@login_required
def upload_page():
    """Upload page"""
    return render_template('upload.html')

@bp.route('/api/upload', methods=['POST'])
@login_required
def api_upload():
    """API endpoint for file upload"""
    
    try:
        # Check if file was sent
        if 'file' not in request.files:
            return jsonify({'success': False, 'message': 'No file provided'}), 400
        
        file = request.files['file']
        
        # Check if file has name
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'}), 400
        
        # Check file type
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'message': f'File type not allowed. Allowed: {", ".join(ALLOWED_EXTENSIONS)}'}), 400
        
        # Save the file
        upload_id = save_uploaded_file(file, current_user.id)
        
        if upload_id:
            return jsonify({
                'success': True,
                'upload_id': upload_id,
                'message': 'File uploaded successfully',
                'redirect': url_for('preview.preview_page', upload_id=upload_id)
            })
        else:
            return jsonify({'success': False, 'message': 'Error saving file to database'}), 500
            
    except Exception as e:
        # Print full error to terminal for debugging
        print("=" * 50)
        print("UPLOAD ERROR:")
        print(traceback.format_exc())
        print("=" * 50)
        return jsonify({'success': False, 'message': f'Server error: {str(e)}'}), 500