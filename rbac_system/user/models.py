from django.db import models

class API(models.Model):
    api_name = models.CharField(max_length=100)

class CustomUser(models.Model):
    ROLES = (
        ('Admin', 'Admin'),
        ('User', 'User'),
        ('Viewer', 'Viewer'),
    )
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=20, choices=ROLES)
    apis = models.ManyToManyField(API)

class profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    role = models.CharField(choices=[('Admin', 'Admin'),('User', 'User'),('Viewer', 'Viewer')], max_length=10)
    token = models.CharField(max_length=750, blank=True, null=True)

