from django.db import models
from django.contrib.auth.models import AbstractUser

# Class for users. No primary key is needed as django automatically adds this.
# By default will have username, password, email
class CustomUser(AbstractUser):
    # todo add primary key to userid so that all users can be identified by their uid
    ROLE_CHOICES = (
        ('admins', 'Admin'),
        ('provider', 'Healthcare Provider'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    is_approved = models.BooleanField(default=False)

class ProviderProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    hospital_name = models.CharField(max_length=100)
    license_number = models.CharField(max_length=100)
    documents = models.FileField(upload_to='provider_docs/')
    # will become true once approved by the admin
    approved_by_admin = models.BooleanField(default=False)

# Class to keep track of all admin logs
class AdminActionLog(models.Model):
    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'admin'})
    action = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)