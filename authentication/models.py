from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=False)
    activation_key = models.CharField(max_length=40, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username", "first_name", "last_name",)

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        ordering = ['first_name']
