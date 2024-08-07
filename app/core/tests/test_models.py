""" testcases for models"""
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

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
            
    def test_new_user_without_email_raises_error(self):
        """raises value error if user is withiout email"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'passwd')
            
    def test_create_superuser(self):
        """create super user"""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'passwd'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        
    def test_create_recipe(self):
        """Test creating a recipe is successful."""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass'
        )
        recipe = models.Recipe.objects.create(
            user = user,
            title='test title',
            time_minutes = 5,
            price = Decimal('100'),
            description = 'sample recipe desc'
        )
        self.assertEqual(str(recipe), recipe.title)