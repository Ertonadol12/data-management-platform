"""
Validation utilities for Data Management Platform
"""

import re

def validate_email(email):
    """
    Validate email format using regex.
    
    Args:
        email (str): Email address to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    if not email:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """
    Validate password strength.
    
    Args:
        password (str): Password to validate
    
    Returns:
        tuple: (is_valid, message)
    """
    if not password:
        return False, "Password cannot be empty"
    
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    
    # Check for at least one digit
    if not any(char.isdigit() for char in password):
        return False, "Password must contain at least one number"
    
    # Check for at least one uppercase letter
    if not any(char.isupper() for char in password):
        return False, "Password must contain at least one uppercase letter"
    
    return True, "Password is valid"

def validate_file_extension(filename, allowed_extensions):
    """
    Validate file extension against allowed list.
    
    Args:
        filename (str): Name of the file
        allowed_extensions (set): Set of allowed extensions
    
    Returns:
        bool: True if extension is allowed, False otherwise
    """
    if not filename:
        return False
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def validate_required_fields(data, required_fields):
    """
    Validate that all required fields are present in data.
    
    Args:
        data (dict): Data dictionary to validate
        required_fields (list): List of required field names
    
    Returns:
        tuple: (is_valid, missing_fields)
    """
    missing = [field for field in required_fields if not data.get(field)]
    return len(missing) == 0, missing