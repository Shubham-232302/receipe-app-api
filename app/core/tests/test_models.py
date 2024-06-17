""" testcases for models"""

from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):
    """Tests Model"""
    
    def test_create_user_with_email_successful(self):
        email="test@example.com"
        password = "password"
        
        user_model = get_user_model().objects.create_user(
            email=email,
            password = password
        )
        self.assertEqual(email, user_model.email)
        self.assertTrue(user_model.check_password(password))
        
    def test_new_user_email_normalized(self):
        """test email is normalised for new users"""
        sample_emails = [
            ['test1@Example.com', 'test1@example.com'],
            ['Test2@example.com', 'Test2@example.com'],
            ['Test3@EXAMPLE.com', 'Test3@example.com']
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, "sample")
            self.assertEqual(user.email, expected)