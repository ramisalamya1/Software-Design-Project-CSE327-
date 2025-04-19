from django.db import models
from django.contrib.auth.models import User
from hospital_search.models import Hospital, Doctor

class Review(models.Model):
    """
    Model representing a hospital/doctor review.
    
    Stores patient reviews with ratings for different aspects of healthcare service
    and optional anonymous posting capability.
    """
    
    # Rating choices from 1 to 5
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    
    # Basic information
    patient_id = models.CharField(max_length=50, null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, null=True, blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)
    anonymous = models.BooleanField(default=False)

    # Rating categories
    service_quality = models.IntegerField(choices=RATING_CHOICES)
    cost_transparency = models.IntegerField(choices=RATING_CHOICES)
    facility_standards = models.IntegerField(choices=RATING_CHOICES)
    treatment_effectiveness = models.IntegerField(choices=RATING_CHOICES)

    # Review content and metadata
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    _is_editable = True

    def __str__(self):
        """String representation of the review"""
        return f"Review by {self.patient_id}"

    @property
    def is_editable(self):
        """Check if review is editable"""
        return self._is_editable

    @is_editable.setter
    def is_editable(self, value):
        """Set review editability status"""
        self._is_editable = value

    def average_rating(self):
        """Calculate average rating across all categories"""
        return (self.service_quality + self.cost_transparency + 
                self.facility_standards + self.treatment_effectiveness) / 4

class ReviewFlag(models.Model):
    """
    Model for flagging inappropriate reviews.
    
    Allows users to report problematic reviews for moderation.
    """
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='flags')
    reported_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    reason = models.TextField()
    reported_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """String representation of the flag"""
        return f"Flag for review {self.review.id}"