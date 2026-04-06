"""
Helper utilities for Data Management Platform
"""

import os
from datetime import datetime

def format_file_size(size_bytes):
    """
    Format file size in human readable format.
    
    Args:
        size_bytes (int): File size in bytes
    
    Returns:
        str: Human readable file size (e.g., "1.5 MB")
    """
    if size_bytes == 0:
        return "0 Bytes"
    
    size_names = ["Bytes", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def format_datetime(dt):
    """
    Format datetime for display.
    
    Args:
        dt (datetime): Datetime object
    
    Returns:
        str: Formatted datetime string
    """
    if dt:
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    return ""

def format_date_short(dt):
    """
    Format date in short format.
    
    Args:
        dt (datetime): Datetime object
    
    Returns:
        str: Short date format (e.g., "Jan 15, 2024")
    """
    if dt:
        return dt.strftime("%b %d, %Y")
    return ""

def get_file_icon(file_type):
    """
    Get Font Awesome icon class for file type.
    
    Args:
        file_type (str): File type (csv, excel, json, etc.)
    
    Returns:
        str: Font Awesome icon class
    """
    icons = {
        'csv': 'fa-file-csv',
        'excel': 'fa-file-excel',
        'xlsx': 'fa-file-excel',
        'xls': 'fa-file-excel',
        'json': 'fa-file-code',
        'txt': 'fa-file-alt',
        'pdf': 'fa-file-pdf',
        'default': 'fa-file'
    }
    return icons.get(file_type, icons['default'])

def truncate_string(text, max_length=50):
    """
    Truncate string to max length and add ellipsis.
    
    Args:
        text (str): Text to truncate
        max_length (int): Maximum length
    
    Returns:
        str: Truncated string
    """
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

def generate_unique_filename(original_filename):
    """
    Generate unique filename using timestamp.
    
    Args:
        original_filename (str): Original filename
    
    Returns:
        str: Unique filename
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    name, ext = os.path.splitext(original_filename)
    return f"{timestamp}_{name}{ext}"