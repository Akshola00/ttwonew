from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from myauth.models import User
from api.models import Organisation
from django.contrib.auth.hashers import make_password

class AuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_registration_success(self):
        response = self.client.post(reverse('auth-register'), {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'password123',
            'phone': '1234567890'
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['message'], 'Registration successful')
        self.assertEqual(response.data['data']['user']['firstName'], 'John')
        self.assertEqual(response.data['data']['user']['email'], 'john.doe@example.com')
        self.assertIn('accessToken', response.data['data'])

        org = Organisation.objects.get(name="John's Organisation")
        self.assertIsNotNone(org)

    def test_user_registration_missing_fields(self):
        response = self.client.post(reverse('auth-register'), {
            'firstName': '',
            'lastName': '',
            'email': '',
            'password': '',
            'phone': '1234567890'
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertTrue(len(response.data['errors']) > 0)

    def test_user_registration_duplicate_email(self):
        User.objects.create(
            first_name='John',
            last_name='Doe',
            email='duplicate@example.com',
            password=make_password('password123'),
            phone='1234567890'
        )

        response = self.client.post(reverse('auth-register'), {
            'firstName': 'Jane',
            'lastName': 'Doe',
            'email': 'duplicate@example.com',
            'password': 'password456',
            'phone': '0987654321'
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(response.data['errors'][0]['message'], 'A user with that email already exists.')

    def test_user_login_success(self):
        user = User.objects.create(
            first_name='Alice',
            last_name='Smith',
            email='alice.smith@example.com',
            password=make_password('password123'),
            phone='1234567890'
        )

        response = self.client.post(reverse('auth-login'), {
            'email': 'alice.smith@example.com',
            'password': 'password123'
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['message'], 'Login successful')
        self.assertIn('accessToken', response.data['data'])
        self.assertEqual(response.data['data']['user']['email'], 'alice.smith@example.com')

    def test_user_login_invalid_credentials(self):
        response = self.client.post(reverse('auth-login'), {
            'email': 'non.existent@example.com',
            'password': 'wrongpassword'
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['status'], 'Bad request')
        self.assertEqual(response.data['message'], 'Authentication failed')

# Ensure to replace 'auth-register' and 'auth-login' with the actual names of your URL patterns
