from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.crypto import get_random_string



class UserManager(BaseUserManager):
    def _create(self,username, password, email, **extra_fields):
        if not username:
            raise ValueError('поле username не может быть пустым')
        if not email:
            raise ValueError('поле email не может быть пустым')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
        
    def create_user(self, username, password, email, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        return self._create(username, password, email, **extra_fields)
    
    def create_superuser(self, username, password, email, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        return self._create(username, password, email, **extra_fields)


class User(AbstractBaseUser):
    username = models.CharField(max_length=15, primary_key=True)
    name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=40, blank=True)
    email = models.EmailField(blank=False)
    about = models.CharField(max_length=100, blank=True, default='папа римский')
    link = models.CharField(max_length=500, blank=True, default=f'{email} and spotify')
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=20, blank=True)
    
    
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.email
    

    def has_module_perms(self, app_lable):
        return self.is_staff
    
    def has_perm(self, perm, obj=None):
        return self.is_staff
    

    def create_activation_code(self):
        code = get_random_string(15)
        self.activation_code = code 
        self.save()