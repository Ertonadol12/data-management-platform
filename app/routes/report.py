"""
Quality Report Routes
"""

from flask import render_template, jsonify, Blueprint
from flask_login import login_required, current_user
from app import db
from app.models.upload import Upload
from app.models.metrics import QualityMetrics
from app.services.file_handler import load_file_to_dataframe
from app.services.quality_checker import generate_quality_metrics

bp = Blueprint('report', __name__, url_prefix='/report')

@bp.route('/<int:upload_id>')
@login_required
def report_page(upload_id):
    """Quality report page"""
    
    upload = Upload.query.get_or_404(upload_id)
    
    if upload.user_id != current_user.id:
        return "Unauthorized", 403
    
    return render_template('report.html', upload=upload)

@bp.route('/api/report/<int:upload_id>')
@login_required
def api_report(upload_id):
    """API endpoint for quality report data"""
    
    upload = Upload.query.get_or_404(upload_id)
    
    if upload.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        # Load the dataframe
        df = load_file_to_dataframe(upload_id)
        
        # Generate metrics
        columns = []
        for col in df.columns:
            # Convert numpy types to Python native types
            null_count = int(df[col].isnull().sum())
            null_percentage = float(round((null_count / len(df)) * 100, 2))
            unique_count = int(df[col].nunique())
            dtype = str(df[col].dtype)
            
            columns.append({
                'name': str(col),
                'null_count': null_count,
                'null_percentage': null_percentage,
                'unique_count': unique_count,
                'data_type': dtype
            })
        
        duplicate_count = int(df.duplicated().sum())
        total_rows = int(len(df))
        total_columns = int(len(df.columns))
        
        return jsonify({
            'success': True,
            'filename': str(upload.original_filename),
            'total_rows': total_rows,
            'total_columns': total_columns,
            'columns': columns,
            'duplicate_count': duplicate_count
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500