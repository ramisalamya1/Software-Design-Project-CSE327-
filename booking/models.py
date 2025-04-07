from django.db import models

class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    date = models.DateTimeField() 

    def __str__(self) -> str:
        return self.title