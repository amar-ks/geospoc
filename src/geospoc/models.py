from django.db import models
# from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User


class UserProfile(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    web_address = models.URLField(max_length=150, blank=True, null=True)
    cover_letter = models.TextField(default='', null=True, blank=True)
    attachment = models.FileField(default='')
    working = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(protocol='IPv4', null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    approved = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
