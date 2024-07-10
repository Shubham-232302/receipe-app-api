""" 
Testcases for recipe APIs
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe

from recipe.serializers import RecipeSerializer


RECIPES_URL = reverse('recipe:recipe-list')

def create_recipe(user, **params):
    """create and return recipe."""
    defaults = {
        'title':'test title',
        'time_minutes':22,
        'price': Decimal('4.5'),
        'description': 'sample desc',
        'link':'https://some/link'
    }
    defaults.update(params)
    
    recipe = Recipe.objects.create(user=user, **defaults)
    return recipe


class PublicRecipeAPITest(TestCase):
    """Test un authenticated API requests"""
    
    def setUp(self):
        self.client = APIClient()
        
    def test_auth_required(self):
        """auth is required to call the api"""
        res = self.client.get(RECIPES_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        
        
class PrivateRecipeAPITest(TestCase):
    """Test authenticated API requests"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'pass12345'
        )
        self.client.force_authenticate(self.user)
        
    def test_retrieve_recipes(self):
        """Test retrieving  a list of  recipes"""
        create_recipe(user=self.user)
        create_recipe(user=self.user)
        
        res =  self.client.get(RECIPES_URL)
        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes,many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        
    def test_retrieve_recipes_limited_to_user(self):
        """Test retrieving  a list of  recipes for the user"""
        other = get_user_model().objects.create_user(
            "other@example.com",
            "passssss1234"
        )
        create_recipe(user=other)
        create_recipe(user=self.user)
        
        res =  self.client.get(RECIPES_URL)
        recipes = Recipe.objects.filter(user = self.user)
        serializer = RecipeSerializer(recipes,many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)