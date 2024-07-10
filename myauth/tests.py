from django.test import TestCase

# Create your tests here.
import unittest
from datetime import datetime, timedelta
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken

class TokenGenerationTestCase(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.access_token = AccessToken.for_user(self.user)

    def test_token_expiry(self):
        expiration_time = self.access_token['exp']
        self.assertLessEqual(expiration_time, datetime.utcnow() + timedelta(minutes=15))
    
    def test_token_user_details(self):
        self.assertEqual(self.access_token['user_id'], self.user.id)
        self.assertEqual(self.access_token['username'], self.user.username)
