# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase
# from .models import Category, Tag, Post
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class CategoryAPITests(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(
#             username='testuser',
#             email='test@example.com',
#             password='testpassword'
#         )
#         self.client.force_authenticate(user=self.user)
    
#     def test_create_category(self):
#         url = reverse('category-list-create')
#         data = {'title': 'Test Category'}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Category.objects.count(), 1)
    
#     # Тесты для других операций (GET, PUT, DELETE) аналогичны

# class TagAPITests(APITestCase):
#     # Аналогично как для CategoryAPITests, но для модели Tag
#     pass

# class PostAPITests(APITestCase):
#     # Аналогично как для CategoryAPITests, но для модели Post
#     pass

# class SerializerTests(TestCase):
#     def test_category_serializer(self):
#         data = {'title': 'Test Category'}
#         serializer = CategorySerializer(data=data)
#         self.assertTrue(serializer.is_valid())
    
#     # Тесты для других сериализаторов (TagSerializer, PostSerializer) аналогичны
