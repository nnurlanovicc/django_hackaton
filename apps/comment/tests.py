from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Comment

User = get_user_model()

class CommentViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.comment_data = {
            'author': self.user.id,  # Замените на актуальные данные автора
            'post': 1,  # Замените на актуальный ID поста
            'body': 'Test comment'
        }
        self.comment = Comment.objects.create(author=self.user, post_id=1, body='Test comment')

    def test_create_comment(self):
        response = self.client.post('/comments/', self.comment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)

    def test_retrieve_comment(self):
        response = self.client.get(f'/comments/{self.comment.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['body'], self.comment.body)

    def test_update_comment(self):
        new_comment_data = {
            'author': self.user.id,
            'post': 1,
            'body': 'Updated comment'
        }
        response = self.client.put(f'/comments/{self.comment.id}/', new_comment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['body'], new_comment_data['body'])

    def test_delete_comment(self):
        response = self.client.delete(f'/comments/{self.comment.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)
