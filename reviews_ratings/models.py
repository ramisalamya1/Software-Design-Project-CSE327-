# reviews/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Hospital(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    
    patient_id = models.CharField(max_length=50)

    def __str__(self):
        return f"Review by {self.patient_id}"
    
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)  # ✅ User is now optional
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, null=True, blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)
    anonymous = models.BooleanField(default=False)

    service_quality = models.IntegerField(choices=RATING_CHOICES)
    cost_transparency = models.IntegerField(choices=RATING_CHOICES)
    facility_standards = models.IntegerField(choices=RATING_CHOICES)
    treatment_effectiveness = models.IntegerField(choices=RATING_CHOICES)

    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_editable(self):
        return timezone.now() <= self.created_at + timedelta(minutes=60)

    def average_rating(self):
        return (self.service_quality + self.cost_transparency + self.facility_standards + self.treatment_effectiveness) / 4

class ReviewFlag(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='flags')
    reason = models.TextField()
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # ✅ Allow NULL
    reported_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Flag on {self.review.id} by {self.reported_by or 'Anonymous'}"