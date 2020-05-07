from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
from rest_framework.views import status


class BaseViewTest(APITestCase):
    def setUp(self):
        client = APIClient()

class UsersTestCase(BaseViewTest):
    def test_user_signup(self):
        response = self.client.post(reverse('signup'), {'username': 'testuser', 'email': 'test@test.com', 'password': 'testpass'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_signup_needs_all_arguments(self):
        response = self.client.post(reverse('signup'), {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_username_should_be_singular(self):
        self.client.post(reverse('signup'), {'username': 'testuser', 'email': 'test@test.com', 'password': 'testpass'})
        response = self.client.post(reverse('signup'), {'username': 'testuser', 'email': 'test@test.com', 'password': 'testpass'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_email_or_password(self):
        response = self.client.post(reverse('signup'), {'username': 'testuser', 'email': 'test', 'password': 'testpass'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)