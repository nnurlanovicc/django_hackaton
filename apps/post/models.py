from django.db import models
from slugify import slugify
from django.contrib.auth import get_user_model
from apps.category.models import Category
from apps.tag.models import Tag


User = get_user_model()

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name='Автор')
    title = models.CharField(max_length=30, verbose_name='Заголовок')
    slug = models.SlugField(max_length=30, blank=True, primary_key=True)
    body = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True, verbose_name='Картинка')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts', verbose_name='Категория')
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.author.username} -> {self.title}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
