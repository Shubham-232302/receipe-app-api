"""
testcases for django admin modification
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client

class AdminSiteTest(TestCase):
    """Tests for django admin"""
    
    def setUp(self):
        """Create User and Client"""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email = "admin@example.com",
            password = "admin@123"
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email = "user@example.com",
            password = "user@123",
            name = "user name"
        )
        
    def test_user_list(self):
        """tests the users registered"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)
        
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)