import unittest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from datetime import datetime, timedelta

class TestAuthEndpoints(unittest.TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = '/auth/register/'
        self.login_url = '/auth/login/'
        self.user_data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'strongpassword'
        }

    def test_register_user_success(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)
        user_id = response.data['user']['id']
        token = response.data['token']

        # Verify token expiration
        token_obj = Token.objects.get(key=token)
        expiration_time = token_obj.created + timedelta(days=1)  # Assuming token expires in 1 day
        self.assertLess(datetime.now(), expiration_time)

    def test_login_user_success(self):
        # First register the user
        register_response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(register_response.status_code, 201)

        # Now attempt to login
        login_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['id'], register_response.data['user']['id'])

    def test_missing_required_fields(self):
        invalid_data = {
            'lastName': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'strongpassword'
        }
        response = self.client.post(self.register_url, invalid_data, format='json')
        self.assertEqual(response.status_code, 422)
        self.assertIn('firstName', response.data['errors'])

    def test_duplicate_email_registration(self):
        # Register the user first
        response1 = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response1.status_code, 201)

        # Try to register again with the same email
        response2 = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response2.status_code, 422)
        self.assertIn('email', response2.data['errors'])

if __name__ == '__main__':
    unittest.main()
