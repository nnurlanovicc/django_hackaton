from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Like

User = get_user_model()

class LikeListCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_like(self):
        data = {
            "post": 1,  # Замените на действительный ID поста
            "comment": 1  # Замените на действительный ID комментария
        }
        response = self.client.post('/likes/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), 1)

    def test_list_likes(self):
        Like.objects.create(author=self.user, post=1, comment=1)
        Like.objects.create(author=self.user, post=2, comment=2)
        response = self.client.get('/likes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

