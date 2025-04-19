from django.db import models
from django.contrib.auth.models import AbstractUser

# Class for users. No primary key is needed as django automatically adds this.
# By default will have username, password, email
class CustomUser(AbstractUser):
    """
    Extended user model that includes roles and approval status.

    Inherits from Django's AbstractUser and adds the following fields:
    
    Attributes:
        role (str): Role of the user. Can be 'admins', 'provider', or 'user'.
        is_approved (bool): Indicates whether the user's registration is approved.
    """
    ROLE_CHOICES = (
        ('admins', 'Admin'),
        ('provider', 'Healthcare Provider'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    is_approved = models.BooleanField(default=False)

class ProviderProfile(models.Model):
    """
    Stores additional information for healthcare provider users.

    Attributes:
        user (OneToOneField): Link to the CustomUser model.
        hospital_name (str): Name of the hospital the provider is affiliated with.
        license_number (str): Professional license number of the provider.
        documents (FileField): File uploads for verification documents.
        approved_by_admin (bool): Indicates whether the profile is verified by an admin.
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    hospital_name = models.CharField(max_length=100)
    license_number = models.CharField(max_length=100)
    documents = models.FileField(upload_to='provider_docs/')
    # will become true once approved by the admin
    approved_by_admin = models.BooleanField(default=False)

# Class to keep track of all admin logs
class AdminActionLog(models.Model):
    """
    Logs actions performed by admin users.

    Attributes:
        admin (ForeignKey): The admin user who performed the action.
        action (TextField): Description of the action taken.
        timestamp (DateTimeField): Date and time of the action (auto-generated).
    """
    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'admin'})
    action = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)