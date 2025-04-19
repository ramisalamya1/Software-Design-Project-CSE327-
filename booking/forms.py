from django import forms
from .models import Patient

class AppointmentForm(forms.ModelForm):
    """Form for creating patient appointments."""
    class Meta:
        model = Patient
        fields = ['name', 'age', 'email', 'phone', 'date']