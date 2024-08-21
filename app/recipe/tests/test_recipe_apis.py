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

from recipe.serializers import RecipeSerializer, RecipeDetailSerializer


RECIPES_URL = reverse('recipe:recipe-list')

def detail_url(recipe_id):
    """Create and return a recipe detail URL"""
    return reverse('recipe:recipe-detail',args=[recipe_id])

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
        
    def test_get_recipe_detail(self):
        """Test to get recipe details"""
        recipe = create_recipe(user=self.user)
        
        url = detail_url(recipe.id)
        res = self.client.get(url)
        
        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)
        
    def test_create_recipe(self):
        """Test creating a recipe"""
        payload  = {
            'title':'sample',
            'time_minutes':30,
            'price': Decimal('6.10'),
        }
        res = self.client.post(RECIPES_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        for k,v in payload.items():
            self.assertEqual(getattr(recipe, k), v)
        self.assertEqual(recipe.user, self.user)
        
            