from app import db
from datetime import datetime

class Upload(db.Model):
    __tablename__ = 'uploads'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    stored_filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(20))
    file_size = db.Column(db.BigInteger)
    row_count = db.Column(db.Integer, default=0)
    column_count = db.Column(db.Integer, default=0)
    status = db.Column(db.String(50), default='pending')
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    processed = db.relationship('ProcessedFile', backref='upload', uselist=False, cascade='all, delete-orphan')
    quality_metrics = db.relationship('QualityMetrics', backref='upload', lazy=True, cascade='all, delete-orphan')