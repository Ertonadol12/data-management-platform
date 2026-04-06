"""
Tests Package for Data Management Platform

This package contains all unit and integration tests.
Run tests with: pytest tests/ -v
"""

# This file makes the 'tests' directory a Python package
# You can add common test utilities here if needed

import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))