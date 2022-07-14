from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.contrib.auth.models import UserManager

class User(AbstractBaseUser):

    username = models.CharField(max_length=32, unique=True)
    email = models.EmailField(unique=True, max_length=64)
    role = models.CharField(max_length=16)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    first_name = models.CharField(max_length=32,default="")
    last_name = models.CharField(max_length=32,default="")

    objects = UserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [] # Email &amp; Password are required by default.

    class Meta:
        db_table = "users"

    def __str__(self):
        return str(self.username)


    