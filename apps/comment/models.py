from django.db import models
from django.contrib.auth import get_user_model
from apps.post.models import Post

User = get_user_model()

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='comments', verbose_name='автор')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='пост')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
