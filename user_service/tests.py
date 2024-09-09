from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserAuthTests(APITestCase):

    def setUp(self):
        # Set up the client and initial user
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass', email='testuser@example.com')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_register_user(self):
        url = reverse('register')  # Using the URL name 'register'
        data = {
            'username': 'newuser',
            'password': 'newpassword',
            'email': 'newuser@example.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)  # The original user and the newly registered one
        self.assertEqual(User.objects.get(username='newuser').email, 'newuser@example.com')

    def test_login_user(self):
        url = reverse('login')  # Using the URL name 'login'
        data = {
            'username': 'testuser',
            'password': 'testpass'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['user_id'], self.user.id)
        self.assertEqual(response.data['username'], 'testuser')

    def test_user_profile_retrieve(self):
        url = reverse('profile')  # Using the URL name 'profile'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)
        self.assertEqual(response.data['email'], self.user.email)

    def test_user_profile_update(self):
        url = reverse('profile')  # Using the URL name 'profile'
        data = {'email': 'updatedemail@example.com'}
        response = self.client.patch(url, data, format='json')  # Partial update
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'updatedemail@example.com')

    def test_user_profile_update_fail(self):
        url = reverse('profile')  # Using the URL name 'profile'
        data = {'email': 'invalid-email'}  # Invalid email format
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
