from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

User = get_user_model()

class AuthenticationTest(APITestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'email': 'test@example.com',
            'name': 'John',
            'last_name': 'Doe',
        }
        self.user = User.objects.create_user(**self.user_data)
        self.activation_code = self.user.activation_code

    def test_registration(self):
        response = self.client.post('/api/v1/register/', self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_activation(self):
        activation_data = {
            'username': self.user_data['username'],
            'code': self.activation_code,
            'email': self.user_data['email'],
        }
        response = self.client.post('/api/v1/activate/', activation_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)
        self.assertEqual(self.user.activation_code, '')

    def test_login(self):
        login_data = {
            'username': self.user_data['username'],
            'password': self.user_data['password'],
        }
        response = self.client.post('/api/v1/login/', login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

    def test_change_password(self):
        self.client.force_authenticate(user=self.user)
        new_password = 'newtestpassword456'
        change_password_data = {
            'old_password': self.user_data['password'],
            'new_password': new_password,
            'new_password_confirm': new_password,
        }
        response = self.client.post('/api/v1/change_pass/', change_password_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(new_password))

    def test_forgot_password(self):
        forgot_password_data = {
            'username': self.user_data['username'],
            'email': self.user_data['email'],
        }
        response = self.client.post('/api/v1/forgot_pass/', forgot_password_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        new_activation_code = self.user.activation_code

        complete_forgot_password_data = {
            'username': self.user_data['username'],
            'code': new_activation_code,
            'password': 'newtestpassword789',
            'password_confirm': 'newtestpassword789',
        }
        response = self.client.post('/api/v1/forgot_pass_comp/', complete_forgot_password_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newtestpassword789'))
