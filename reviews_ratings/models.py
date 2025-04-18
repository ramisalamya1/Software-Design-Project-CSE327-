from django.db import models
from django.contrib.auth.models import User
from hospital_search.models import Hospital, Doctor

class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    
    patient_id = models.CharField(max_length=50, null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, null=True, blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)
    anonymous = models.BooleanField(default=False)

    service_quality = models.IntegerField(choices=RATING_CHOICES)
    cost_transparency = models.IntegerField(choices=RATING_CHOICES)
    facility_standards = models.IntegerField(choices=RATING_CHOICES)
    treatment_effectiveness = models.IntegerField(choices=RATING_CHOICES)

    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    _is_editable = True

    def __str__(self):
        return f"Review by {self.patient_id}"

    @property
    def is_editable(self):
        return self._is_editable

    @is_editable.setter
    def is_editable(self, value):
        self._is_editable = value

    def average_rating(self):
        return (self.service_quality + self.cost_transparency + 
                self.facility_standards + self.treatment_effectiveness) / 4

class ReviewFlag(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='flags')
    reported_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    reason = models.TextField()
    reported_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Flag for review {self.review.id}"