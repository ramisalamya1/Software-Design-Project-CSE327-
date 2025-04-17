"""
Model definitions for package customization features.
Each model represents a key component of a medical travel package.
"""

from django.db import models

class Hospital(models.Model):
    """
    Model representing a hospital with basic info.

    Attributes:
        name (str): Name of the hospital.
        city (str): City where the hospital is located.
        country (str): Country where the hospital is located.
        treatment_type (str): Type of treatment.
        cost_estimate (Decimal): Estimated cost for treatment.
        accreditation (str): Hospital accreditation (e.g., JCI, NABH).
    """
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    treatment_type = models.CharField(max_length=100, default='General')
    cost_estimate = models.DecimalField(max_digits=10, decimal_places=2)
    accreditation = models.CharField(max_length=100, blank=True, null=True)  # New field
    accepts_insurance = models.BooleanField(default=True)

    def __str__(self):
        return self.name



class Accommodation(models.Model):
    """
    Accommodation options near hospitals.

    Attributes:
        name (str): Name of the accommodation.
        type (str): Type (hotel, guest house, etc.).
        distance_to_hospital (Decimal): Distance in km.
        cost_per_night (Decimal): Cost per night.
        amenities (str): Features included.
        available (bool): Availability status.
    """
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=100)
    distance_to_hospital = models.DecimalField(max_digits=5, decimal_places=2)
    cost_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    amenities = models.TextField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.type})"


class Transport(models.Model):
    """
    Transportation service details.

    Attributes:
        type (str): Vehicle type.
        provider (str): Service provider.
        cost_per_km (Decimal): Cost per kilometer.
        available (bool): Availability status.
    """
    type = models.CharField(max_length=100)
    provider = models.CharField(max_length=255)
    cost_per_km = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.type} by {self.provider}"


class TravelAssistance(models.Model):
    """
    Services for visa, guides, translators, etc.

    Attributes:
        service_type (str): Type of service.
        provider (str): Provider name.
        cost (Decimal): Service cost.
        description (str): Details of service.
    """
    service_type = models.CharField(max_length=100)
    provider = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return f"{self.service_type} - {self.provider}"


class DietaryOption(models.Model):
    """
    Meal plan options (e.g., halal, vegetarian).

    Attributes:
        name (str): Meal type.
        description (str): Meal details.
        cost_per_day (Decimal): Daily cost.
        available (bool): If available.
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    cost_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class RehabilitationService(models.Model):
    """
    Recovery services post-treatment.

    Attributes:
        name (str): Service name.
        type (str): Physiotherapy, yoga, etc.
        provider (str): Who provides the service.
        cost_per_session (Decimal): Cost per session.
        duration (int): Duration in minutes.
    """
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=100)
    provider = models.CharField(max_length=255)
    cost_per_session = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.type})"


class MedicalPackage(models.Model):
    """
    Custom medical package containing all selected services.

    Attributes:
        user_name (str): Name of the patient.
        hospital (Hospital): Chosen hospital.
        treatment_date (date): Scheduled treatment date.
        accommodation (Accommodation): Lodging.
        transport (Transport): Transportation.
        travel_assistance (M2M): Extra services.
        dietary_option (DietaryOption): Meal preference.
        rehabilitation (RehabilitationService): Rehab service.
        total_cost (Decimal): Final cost.
        created_at (datetime): Creation timestamp.
        notes (str): Additional notes.
    """
    user_name = models.CharField(max_length=255)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    treatment_date = models.DateField()
    accommodation = models.ForeignKey(Accommodation, on_delete=models.SET_NULL, null=True)
    transport = models.ForeignKey(Transport, on_delete=models.SET_NULL, null=True)
    travel_assistance = models.ManyToManyField(TravelAssistance)
    dietary_option = models.ForeignKey(DietaryOption, on_delete=models.SET_NULL, null=True)
    rehabilitation = models.ForeignKey(RehabilitationService, on_delete=models.SET_NULL, null=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Package for {self.user_name} at {self.hospital.name}"