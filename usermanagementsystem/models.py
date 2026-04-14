from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    
    # Track who created the user (Ownership)    
    created_by = models.ForeignKey(
        'self', on_delete=models.SET_NULL, 
        null=True, blank=True, related_name='created_users'
    )
    
    # Admin can assign a manager to a user
    manager = models.ForeignKey(
        'self', on_delete=models.SET_NULL, 
        null=True, blank=True, related_name='managed_users'
    )

    is_deleted = models.BooleanField(default=False)
    # Note: last_login is already built into AbstractUser! 
    # We will use user.last_login in the templates.

    def __str__(self):
        return f"{self.username} ({self.role})"