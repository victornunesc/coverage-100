from django.db import models
from django.contrib.auth.models import AbstractUser

from accounts.managers import AccountManager


class Account(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_seller = models.BooleanField()

    is_staff = None
    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = AccountManager()
