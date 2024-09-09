from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField()
    first_name = models.CharField(max_length=300)
    last_name = models.CharField(max_length=300)
    date_of_birth = models.DateField(default="2024-09-07")
    gender = models.CharField(max_length=100, choices=[('male', 'Male'), ('female', 'Female'), ('others', 'Others')])
    address = models.CharField(max_length=300)

    REQUIRED_FIELDS = []

    objects = UserManager()
        
    def __str__(self):
        return self.email