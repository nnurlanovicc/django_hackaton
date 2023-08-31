from django.db import models
from django.contrib.auth import get_user_model
from apps.post.models import Post
from apps.comment.models import Comment

User = get_user_model()


class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['author', 'post'] 
        constraints = [models.UniqueConstraint(fields=['author','comment'],name='unique_like_comment_author')]

    def __str__(self) -> str:
        return f'liked by: {self.author.username}'




