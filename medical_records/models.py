from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# from django_cryptography.fields import EncryptedTextField  # For encrypting data


class Category(models.Model):
    """
    Represents a category for organizing medical records.
    
    Attributes:
        name (str): The name of the category (max length: 100 chars)
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MedicalRecord(models.Model):
    """
    Represents a medical record document with associated metadata.
    
    Attributes:
        user (ForeignKey): The user who owns this record
        title (str): Title of the medical record
        record_type (str): Type of medical record (from RECORD_TYPES choices)
        description (TextField): Detailed description of the record
        record_file (FileField): The actual medical record document
        category (ForeignKey): Optional category classification
        date_created (DateTimeField): When the record was created
        version_history (JSONField): List tracking document versions
        share_token (str): Token for sharing record with others
    """
    RECORD_TYPES = [
        ('prescription', 'Prescription'),
        ('blood_test', 'Blood Test'),
        ('diagnostic_report', 'Diagnostic Report'),
        ('doctor_note', 'Doctor\'s Note'),
        ('surgery_summary', 'Surgery Summary'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    record_type = models.CharField(choices=RECORD_TYPES, max_length=100)
    
    # Commented out the encryption for now, using a regular text field
    description = models.TextField()  # Regular text field for description
    record_file = models.FileField(upload_to='medical_records/')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    version_history = models.JSONField(default=list)  # To track version history
    share_token = models.CharField(max_length=64, blank=True, null=True)  

    def __str__(self):
        return self.title


class Reminder(models.Model):
    """
    Represents a reminder associated with a medical record.
    
    Attributes:
        user (ForeignKey): The user who created the reminder
        medical_record (ForeignKey): The associated medical record
        reminder_date (DateTimeField): When the reminder should trigger
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE)
    reminder_date = models.DateTimeField()

    def __str__(self):
        return f"Reminder for {self.medical_record.title} on {self.reminder_date}"