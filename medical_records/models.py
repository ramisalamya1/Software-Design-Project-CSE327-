from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# from django_cryptography.fields import EncryptedTextField  # For encrypting data


# Constants for model configuration
MAX_CATEGORY_NAME_LENGTH = 100
MAX_TITLE_LENGTH = 255
MAX_RECORD_TYPE_LENGTH = 100
MAX_SHARE_TOKEN_LENGTH = 64
UPLOAD_PATH = 'medical_records/'

# Record type choices constant
RECORD_TYPES = [
    ('prescription', 'Prescription'),
    ('blood_test', 'Blood Test'),
    ('diagnostic_report', 'Diagnostic Report'),
    ('doctor_note', 'Doctor\'s Note'),
    ('surgery_summary', 'Surgery Summary'),
]


class Category(models.Model):  # PascalCase for class name (correct)
    """
    Represents a category for organizing medical records.
    
    Attributes:
        name (str): The name of the category (max length: 100 chars)
    """
    name = models.CharField(max_length=MAX_CATEGORY_NAME_LENGTH)  # snake_case for field name

    def __str__(self):
        return self.name


class MedicalRecord(models.Model):  # PascalCase for class name (correct)
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # snake_case for field names
    title = models.CharField(max_length=MAX_TITLE_LENGTH)
    record_type = models.CharField(
        choices=RECORD_TYPES,
        max_length=MAX_RECORD_TYPE_LENGTH
    )
    description = models.TextField()
    record_file = models.FileField(upload_to=UPLOAD_PATH)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    date_created = models.DateTimeField(default=timezone.now)
    version_history = models.JSONField(default=list)
    share_token = models.CharField(
        max_length=MAX_SHARE_TOKEN_LENGTH,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title


class Reminder(models.Model):  # PascalCase for class name (correct)
    """
    Represents a reminder associated with a medical record.
    
    Attributes:
        user (ForeignKey): The user who created the reminder
        medical_record (ForeignKey): The associated medical record
        reminder_date (DateTimeField): When the reminder should trigger
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # snake_case for field names
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE)
    reminder_date = models.DateTimeField()

    def __str__(self):
        return f"Reminder for {self.medical_record.title} on {self.reminder_date}"