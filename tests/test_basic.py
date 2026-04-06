"""
Basic tests for Data Management Platform
"""

import unittest
import sys
import os
import tempfile

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models.user import User
from app.models.upload import Upload
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class BasicTests(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment"""
        # Create test app
        self.app = create_app('testing')
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        
        # Create test client
        self.client = self.app.test_client()
        
        # Push context
        self.ctx = self.app.app_context()
        self.ctx.push()
        
        # Create all tables
        db.create_all()
        
        # Create a test user
        password_hash = bcrypt.generate_password_hash('test123').decode('utf-8')
        self.test_user = User(
            username='testuser',
            email='test@example.com',
            password_hash=password_hash,
            full_name='Test User'
        )
        db.session.add(self.test_user)
        db.session.commit()
    
    def tearDown(self):
        """Clean up after tests"""
        db.session.remove()
        db.drop_all()
        self.ctx.pop()
    
    def test_app_exists(self):
        """Test that app is created"""
        self.assertIsNotNone(self.app)
    
    def test_home_page_redirects(self):
        """Test home page redirects to login"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
    
    def test_login_page_loads(self):
        """Test login page loads"""
        response = self.client.get('/auth/login')
        self.assertEqual(response.status_code, 200)
    
    def test_register_page_loads(self):
        """Test register page loads"""
        response = self.client.get('/auth/register')
        self.assertEqual(response.status_code, 200)
    
    def test_dashboard_requires_login(self):
        """Test dashboard redirects to login when not authenticated"""
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 302)
    
    def test_login_with_correct_credentials(self):
        """Test login with correct credentials"""
        response = self.client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'test123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_login_with_wrong_password(self):
        """Test login with wrong password"""
        response = self.client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'wrongpassword'
        })
        # Should stay on login page
        self.assertIn(b'Login', response.data)

if __name__ == '__main__':
    unittest.main()