"""
Export service - CSV, Excel, JSON export functionality
"""

import os
import pandas as pd
from datetime import datetime
from flask import current_app

def export_to_csv(df, filepath):
    """Export DataFrame to CSV"""
    df.to_csv(filepath, index=False)
    return filepath

def export_to_excel(df, filepath):
    """Export DataFrame to Excel"""
    df.to_excel(filepath, index=False)
    return filepath

def export_to_json(df, filepath):
    """Export DataFrame to JSON"""
    df.to_json(filepath, orient='records', indent=2)
    return filepath

def export_cleaned_data(upload_id, df, format_type):
    """
    Export cleaned data in specified format.
    
    Args:
        upload_id (int): Upload ID
        df (DataFrame): Data to export
        format_type (str): 'csv', 'excel', or 'json'
    
    Returns:
        str: Path to exported file
    """
    
    upload_folder = current_app.config['UPLOAD_FOLDER']
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if format_type == 'csv':
        filename = f"export_{timestamp}.csv"
        filepath = os.path.join(upload_folder, filename)
        export_to_csv(df, filepath)
    elif format_type == 'excel':
        filename = f"export_{timestamp}.xlsx"
        filepath = os.path.join(upload_folder, filename)
        export_to_excel(df, filepath)
    elif format_type == 'json':
        filename = f"export_{timestamp}.json"
        filepath = os.path.join(upload_folder, filename)
        export_to_json(df, filepath)
    else:
        raise ValueError(f"Unsupported format: {format_type}")
    
    return filepath, filename