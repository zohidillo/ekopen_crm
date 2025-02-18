from django.db import models
import src.core.models.contants as cons
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    role = models.CharField(max_length=50, choices=cons.CONSTANTS.ROLE.CHOICES, null=True, blank=True)
    password_2 = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return f"{self.username} - {self.role}"

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
