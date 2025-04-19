from django.db import models

class Patient(models.Model):
    """
    Represents a patient who has booked an appointment.

    Attributes:
        name (str): The full name of the patient.
        age (int): The patient's age.
        email (str): The patient's email address.
        phone (str): The patient's phone number.
        date (datetime): The date and time of the booking.
    """
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    date = models.DateTimeField() 

    def __str__(self) -> str:
        """
        Returns a string representation of the patient.

        Returns:
            str: The name of the patient.
        """
        return self.title