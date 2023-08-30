# Generated by Django 4.2.4 on 2023-08-30 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=20)),
                ('last_name', models.CharField(blank=True, max_length=40)),
                ('email', models.EmailField(max_length=254)),
                ('about', models.CharField(blank=True, default='папа римский', max_length=100)),
                ('link', models.CharField(blank=True, default='<django.db.models.fields.EmailField> and spotify', max_length=500)),
                ('is_active', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('activation_code', models.CharField(blank=True, max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]