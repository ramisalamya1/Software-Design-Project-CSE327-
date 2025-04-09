# reviews/forms.py

from django import forms
from .models import Review, ReviewFlag

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            'hospital', 'doctor', 'anonymous',
            'service_quality', 'cost_transparency',
            'facility_standards', 'treatment_effectiveness', 'text'
        ]

class ReviewFlagForm(forms.ModelForm):
    class Meta:
        model = ReviewFlag
        fields = ['reason']
