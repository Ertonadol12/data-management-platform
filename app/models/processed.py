from app import db
from datetime import datetime

class ProcessedFile(db.Model):
    __tablename__ = 'processed_files'
    
    id = db.Column(db.Integer, primary_key=True)
    upload_id = db.Column(db.Integer, db.ForeignKey('uploads.id', ondelete='CASCADE'), nullable=False)
    cleaned_filename = db.Column(db.String(255))
    report_filename = db.Column(db.String(255))
    rows_original = db.Column(db.Integer)
    rows_after_clean = db.Column(db.Integer)
    rows_removed = db.Column(db.Integer)
    processing_time = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)