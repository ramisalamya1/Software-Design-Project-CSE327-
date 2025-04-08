from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet  # type: ignore
import base64

# Simple symmetric encryption
key = base64.urlsafe_b64encode(b'0123456789abcdef0123456789abcdef')  # 32 bytes key
cipher = Fernet(key)

def encrypt(data):
    return cipher.encrypt(data.encode()).decode()

def decrypt(data):
    return cipher.decrypt(data.encode()).decode()

RECORD_TYPES = [
    ('prescription', 'Prescription'),
    ('diagnostic', 'Diagnostic Report'),
    ('doctors_note', 'Doctor\'s Note'),
    ('surgery', 'Surgery/Discharge Summary'),
    ('other', 'Other'),
]

class MedicalRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    record_type = models.CharField(max_length=50, choices=RECORD_TYPES)
    date = models.DateField()
    encrypted_file = models.FileField(upload_to='records/')
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    version = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.title} - {self.user.username}"

class RecordVersion(models.Model):
    record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='versions')
    file = models.FileField(upload_to='records/versioned/')
    updated_at = models.DateTimeField(auto_now_add=True)
    version_number = models.IntegerField()

    def __str__(self):
        return f"{self.record.title} - v{self.version_number}"

class SharedAccess(models.Model):
    record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255, unique=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"Shared access for {self.record.title}"

class Reminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE)
    reminder_date = models.DateTimeField()
    message = models.CharField(max_length=255)

    def __str__(self):
        return f"Reminder for {self.user.username} on {self.reminder_date}"
