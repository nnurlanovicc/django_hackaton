# Generated by Django 4.2.4 on 2023-09-01 06:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('post', '0001_initial'),
        ('comment', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comment.comment')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post.post')),
            ],
        ),
        migrations.AddConstraint(
            model_name='like',
            constraint=models.UniqueConstraint(fields=('author', 'comment'), name='unique_like_comment_author'),
        ),
        migrations.AlterUniqueTogether(
            name='like',
            unique_together={('author', 'post')},
        ),
    ]
