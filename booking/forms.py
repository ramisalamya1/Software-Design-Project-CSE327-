from django import forms
from .models import Patient

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'age', 'email', 'phone', 'date']