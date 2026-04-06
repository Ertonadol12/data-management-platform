"""
Quality checking service - metrics calculation
"""

import pandas as pd
import numpy as np
from app import db
from app.models.metrics import QualityMetrics

def generate_quality_metrics(df):
    """Calculate quality metrics for DataFrame"""
    
    metrics = {}
    total_rows = len(df)
    
    for column in df.columns:
        # Convert column name to string
        col_name = str(column)
        
        # Convert numpy types to Python native types
        null_count = int(df[column].isnull().sum())
        null_percentage = float((null_count / total_rows) * 100) if total_rows > 0 else 0.0
        unique_count = int(df[column].nunique())
        
        # Get data type as string
        dtype = str(df[column].dtype)
        
        metrics[col_name] = {
            'null_count': null_count,
            'null_percentage': round(null_percentage, 2),
            'unique_count': unique_count,
            'data_type': dtype
        }
    
    duplicate_count = int(df.duplicated().sum())
    duplicate_percentage = float((duplicate_count / total_rows) * 100) if total_rows > 0 else 0.0
    
    return {
        'column_metrics': metrics,
        'total_rows': total_rows,
        'duplicate_count': duplicate_count,
        'duplicate_percentage': round(duplicate_percentage, 2)
    }

def save_quality_report(upload_id, metrics):
    """Save quality metrics to database"""
    
    # Delete existing metrics for this upload
    QualityMetrics.query.filter_by(upload_id=upload_id).delete()
    
    for col, col_metrics in metrics['column_metrics'].items():
        qm = QualityMetrics(
            upload_id=upload_id,
            column_name=str(col),
            null_count=int(col_metrics['null_count']),
            null_percentage=float(col_metrics['null_percentage']),
            duplicate_count=int(metrics['duplicate_count']),
            unique_count=int(col_metrics['unique_count']),
            data_type=str(col_metrics['data_type'])
        )
        db.session.add(qm)
    
    db.session.commit()