from django.db import models

class Facility(models.Model):
    """
    Model representing a facility offered by a hospital.

    Attributes:
        name (str): The name of the facility (e.g., ICU, WiFi, Ambulance).
    """

    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        """
        Returns a string representation of the Facility.
        """
        return self.name


class Hospital(models.Model):
    """
    Model representing a hospital with basic info and associated details.

    Attributes:
        name (str): Name of the hospital.
        city (str): City where the hospital is located.
        country (str): Country where the hospital is located.
        accreditation (str): Type of accreditation the hospital holds.
        treatment_type (str): Type of treatment the hospital specializes in.
        cost_estimate (decimal): Estimated cost for the treatment.
        facilities (ManyToMany): List of facilities offered.
        accepts_insurance (bool): Whether the hospital accepts insurance.
        is_available (bool): Real-time availability status.
    """

    name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    accreditation = models.CharField(max_length=255, blank=True)
    treatment_type = models.CharField(max_length=100, default='General')
    cost_estimate = models.DecimalField(max_digits=10, decimal_places=2)
    facilities = models.ManyToManyField(Facility, related_name="hospitals")
    accepts_insurance = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)

    def __str__(self) -> str:
        """
        Returns a string representation of the Hospital.
        """
        return self.name


class Doctor(models.Model):
    """
    Model representing a doctor working in a hospital.

    Attributes:
        hospital (ForeignKey): The hospital the doctor is affiliated with.
        name (str): Full name of the doctor.
        specialty (str): Doctor's area of specialization (e.g., Cardiology).
        profile (text): Brief profile/biography of the doctor.
        rating (float): Average rating of the doctor.
    """

    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='doctors')
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    profile = models.TextField()
    rating = models.FloatField(default=0.0)

    def __str__(self) -> str:
        """
        Returns a string representation of the Doctor.
        """
        return self.name


class Review(models.Model):
    """
    Model representing a patient review for a hospital.

    Attributes:
        hospital (ForeignKey): Hospital the review is associated with.
        user_name (str): Name of the reviewer.
        content (text): Review content.
        rating (int): Rating given (usually between 1 and 5).
    """

    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='reviews')
    user_name = models.CharField(max_length=100)
    content = models.TextField()
    rating = models.PositiveIntegerField()

    def __str__(self) -> str:
        """
        Returns a string representation of the Review.
        """
        return f"{self.user_name}'s Review"