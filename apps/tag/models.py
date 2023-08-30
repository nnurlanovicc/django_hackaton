from django.db import models
from slugify import slugify

class Tag(models.Model):
    title = models.CharField(max_length=30)
    slug = models.SlugField(max_length=30, primary_key=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
