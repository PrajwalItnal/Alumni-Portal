# Create your models here.
from django.db import models

class User(models.Model):
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('STUDENT', 'Student'),
        ('ALUMNI', 'Alumni'),
    ]
    user_id = models.AutoField(primary_key=True)
    register_id = models.CharField(max_length = 14, unique=True)
    username = models.CharField(max_length = 25)
    password = models.CharField(max_length = 255)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length = 10, choices = ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user"

    def __str__(self):
        return self.username

