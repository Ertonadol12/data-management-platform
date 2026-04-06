"""
Data Preview Routes
"""

import pandas as pd
from flask import render_template, jsonify, Blueprint
from flask_login import login_required, current_user
from app import db
from app.models.upload import Upload
from app.services.file_handler import load_file_to_dataframe

bp = Blueprint('preview', __name__, url_prefix='/preview')

@bp.route('/<int:upload_id>')
@login_required
def preview_page(upload_id):
    """Data preview page"""
    
    upload = Upload.query.get_or_404(upload_id)
    
    # Verify ownership
    if upload.user_id != current_user.id:
        return "Unauthorized", 403
    
    return render_template('preview.html', upload=upload)

@bp.route('/api/preview/<int:upload_id>')
@login_required
def api_preview(upload_id):
    """API endpoint for preview data"""
    
    upload = Upload.query.get_or_404(upload_id)
    
    if upload.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        df = load_file_to_dataframe(upload_id)
        
        # Get column info
        columns = []
        for col in df.columns:
            columns.append({
                'name': col,
                'dtype': str(df[col].dtype),
                'null_count': int(df[col].isnull().sum()),
                'null_percentage': round((df[col].isnull().sum() / len(df)) * 100, 2),
                'unique_count': int(df[col].nunique())
            })
        
        # Get first 100 rows
        preview_data = df.head(100).fillna('').to_dict(orient='records')
        
        return jsonify({
            'success': True,
            'columns': columns,
            'preview_data': preview_data,
            'total_rows': len(df),
            'total_columns': len(df.columns)
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500