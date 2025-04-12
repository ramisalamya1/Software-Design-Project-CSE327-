from django.db import models
from hospital_search.models import Hospital

class ComparisonRecord(models.Model):
    """
    Stores the comparison between hospitals requested by a user.
    """
    selected_hospitals = models.ManyToManyField(Hospital)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comparison #{self.id} - {self.created_at.strftime('%Y-%m-%d')}"

class HospitalStats(models.Model):
    """
    Stores statistical and additional data for hospitals.
    """
    hospital = models.OneToOneField(Hospital, on_delete=models.CASCADE, related_name="comparison_stats")
    recovery_rate = models.FloatField(help_text="Recovery rate in percentage")
    icu_capacity = models.PositiveIntegerField()
    has_robotic_surgery = models.BooleanField(default=False)
    medical_equipment = models.TextField()
    post_treatment_support = models.TextField()
    accreditation = models.CharField(max_length=255)

    def __str__(self):
        return f"Stats for {self.hospital.name}"