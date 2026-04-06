"""
Data Cleaning Routes
"""

import pandas as pd
import time
from flask import render_template, jsonify, request
from flask_login import login_required, current_user
from app import db
from app.models.upload import Upload
from app.models.processed import ProcessedFile
from app.services.file_handler import load_file_to_dataframe, save_cleaned_file
from app.services.data_cleaner import DataCleaner
from app.services.quality_checker import generate_quality_metrics, save_quality_report
from flask import Blueprint

bp = Blueprint('clean', __name__, url_prefix='/clean')

@bp.route('/<int:upload_id>')
@login_required
def clean_page(upload_id):
    """Data cleaning page"""
    
    upload = Upload.query.get_or_404(upload_id)
    
    if upload.user_id != current_user.id:
        return "Unauthorized", 403
    
    return render_template('clean.html', upload=upload)

@bp.route('/api/clean/<int:upload_id>', methods=['POST'])
@login_required
def api_clean(upload_id):
    """API endpoint for cleaning operations"""
    
    upload = Upload.query.get_or_404(upload_id)
    
    if upload.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    operations = data.get('operations', [])
    
    try:
        start_time = time.time()
        df = load_file_to_dataframe(upload_id)
        rows_original = len(df)
        
        cleaner = DataCleaner(df)
        
        # Apply cleaning operations
        for op in operations:
            op_type = op.get('type')
            
            if op_type == 'remove_duplicates':
                subset = op.get('subset')
                cleaner.remove_duplicates(subset)
            
            elif op_type == 'fill_missing':
                column = op.get('column')
                method = op.get('method')
                value = op.get('value')
                cleaner.fill_missing(column, method, value)
            
            elif op_type == 'standardize':
                columns = op.get('columns', [])
                action = op.get('action')
                cleaner.standardize_text_columns(columns, action)
            
            elif op_type == 'convert_type':
                column = op.get('column')
                new_type = op.get('new_type')
                cleaner.convert_type(column, new_type)
            
            elif op_type == 'remove_outliers':
                column = op.get('column')
                method = op.get('method', 'iqr')
                cleaner.remove_outliers(column, method)
        
        df_cleaned = cleaner.get_clean_df()
        rows_after = len(df_cleaned)
        rows_removed = rows_original - rows_after
        processing_time = time.time() - start_time
        
        # Save cleaned file
        cleaned_filename = save_cleaned_file(upload_id, df_cleaned)
        
        # Generate quality metrics
        metrics = generate_quality_metrics(df_cleaned)
        save_quality_report(upload_id, metrics)
        
        # Update upload status
        upload.status = 'completed'
        db.session.commit()
        
        # Save processed record
        processed = ProcessedFile(
            upload_id=upload_id,
            cleaned_filename=cleaned_filename,
            rows_original=rows_original,
            rows_after_clean=rows_after,
            rows_removed=rows_removed,
            processing_time=processing_time
        )
        db.session.add(processed)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'rows_original': rows_original,
            'rows_after': rows_after,
            'rows_removed': rows_removed,
            'processing_time': round(processing_time, 2),
            'message': 'Cleaning completed successfully'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500