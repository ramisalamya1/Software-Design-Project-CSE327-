# reviews/forms.py

from django import forms
from .models import Review, ReviewFlag

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            'hospital', 'doctor', 'anonymous',
            'service_quality', 'cost_transparency',
            'facility_standards', 'treatment_effectiveness', 'text', 'patient_id',
        ]
        widgets = {
            'text': forms.Textarea(attrs={'rows': 5, 'cols': 40, 'placeholder': 'Write your experience here...'}),
        }

class ReviewFlagForm(forms.ModelForm):
    class Meta:
        model = ReviewFlag
        fields = ['reason']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 3, 'cols': 40, 'placeholder': 'Explain why you are flagging this review.'}),
        }
