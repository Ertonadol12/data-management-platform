"""
File handling service - upload, save, load, delete
"""

import os
import pandas as pd
from werkzeug.utils import secure_filename
from datetime import datetime
from app import db
from app.models.upload import Upload
from flask import current_app

def save_uploaded_file(file, user_id):
    """Save uploaded file to disk and database"""
    
    try:
        from flask import current_app
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        original_filename = secure_filename(file.filename)
        stored_filename = f"{timestamp}_{original_filename}"
        
        upload_folder = current_app.config['UPLOAD_FOLDER']
        
        # Ensure upload folder exists
        os.makedirs(upload_folder, exist_ok=True)
        
        filepath = os.path.join(upload_folder, stored_filename)
        
        # Save file to disk
        file.save(filepath)
        
        # Detect file type
        ext = original_filename.rsplit('.', 1)[1].lower()
        if ext == 'csv':
            file_type = 'csv'
        elif ext in ['xlsx', 'xls']:
            file_type = 'excel'
        elif ext == 'json':
            file_type = 'json'
        else:
            file_type = 'unknown'
        
        # Save to database
        upload = Upload(
            user_id=user_id,
            original_filename=original_filename,
            stored_filename=stored_filename,
            file_type=file_type,
            file_size=os.path.getsize(filepath),
            status='uploaded'
        )
        
        db.session.add(upload)
        db.session.commit()
        
        return upload.id
        
    except Exception as e:
        print(f"Error saving file: {e}")
        import traceback
        traceback.print_exc()
        return None

def get_file_info(upload_id):
    """Get file information by upload ID"""
    
    upload = Upload.query.get(upload_id)
    if not upload:
        return None
    
    return {
        'id': upload.id,
        'original_filename': upload.original_filename,
        'stored_filename': upload.stored_filename,
        'file_type': upload.file_type,
        'file_size': upload.file_size,
        'row_count': upload.row_count,
        'column_count': upload.column_count,
        'status': upload.status,
        'uploaded_at': upload.uploaded_at
    }

def load_file_to_dataframe(upload_id):
    """Load file into pandas DataFrame"""
    
    upload = Upload.query.get(upload_id)
    upload_folder = current_app.config['UPLOAD_FOLDER']
    filepath = os.path.join(upload_folder, upload.stored_filename)
    
    if upload.file_type == 'csv':
        # Specify encoding to avoid bytes issues
        df = pd.read_csv(filepath, encoding='utf-8')
    elif upload.file_type == 'excel':
        df = pd.read_excel(filepath)
    elif upload.file_type == 'json':
        df = pd.read_json(filepath)
    else:
        raise ValueError(f"Unsupported file type: {upload.file_type}")
    
    # Convert any bytes columns to strings
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].astype(str)
    
    # Update row and column count
    upload.row_count = int(len(df))
    upload.column_count = int(len(df.columns))
    db.session.commit()
    
    return df

def save_cleaned_file(upload_id, df):
    """Save cleaned DataFrame to file"""
    
    upload = Upload.query.get(upload_id)
    upload_folder = current_app.config['UPLOAD_FOLDER']
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    name, ext = os.path.splitext(upload.original_filename)
    cleaned_filename = f"cleaned_{timestamp}_{name}{ext}"
    filepath = os.path.join(upload_folder, cleaned_filename)
    
    # Save based on original file type
    if upload.file_type == 'csv':
        df.to_csv(filepath, index=False)
    elif upload.file_type == 'excel':
        df.to_excel(filepath, index=False)
    elif upload.file_type == 'json':
        df.to_json(filepath, orient='records', indent=2)
    
    return cleaned_filename

def delete_file(upload_id):
    """Delete file from disk and database"""
    
    upload = Upload.query.get(upload_id)
    if not upload:
        return False
    
    upload_folder = current_app.config['UPLOAD_FOLDER']
    filepath = os.path.join(upload_folder, upload.stored_filename)
    
    if os.path.exists(filepath):
        os.remove(filepath)
    
    db.session.delete(upload)
    db.session.commit()
    
    return True

def update_upload_status(upload_id, status):
    """Update upload status"""
    
    upload = Upload.query.get(upload_id)
    if upload:
        upload.status = status
        db.session.commit()
        return True
    return False