from app import db

class QualityMetrics(db.Model):
    __tablename__ = 'quality_metrics'
    
    id = db.Column(db.Integer, primary_key=True)
    upload_id = db.Column(db.Integer, db.ForeignKey('uploads.id', ondelete='CASCADE'), nullable=False)
    column_name = db.Column(db.String(100))
    null_count = db.Column(db.Integer, default=0)
    null_percentage = db.Column(db.Float, default=0)
    duplicate_count = db.Column(db.Integer, default=0)
    unique_count = db.Column(db.Integer, default=0)
    data_type = db.Column(db.String(50))