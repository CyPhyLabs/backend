from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginViewTest(APITestCase):
    def test_login_user(self):
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'testpassword123',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)