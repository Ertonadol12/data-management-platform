#!/usr/bin/env python3
"""
Database initialization script for Data Management Platform
"""

from app import create_app, db
from app.models import User, Upload, ProcessedFile, QualityMetrics, UserSession

print("Creating database...")

app = create_app()

with app.app_context():
    db.create_all()
    print("Database created successfully!")

print("Tables created:")
print("  - users")
print("  - uploads")
print("  - processed_files")
print("  - quality_metrics")
print("  - user_sessions")