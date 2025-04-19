"""
Forms for handling review and flag submissions.
Provides form classes for creating/editing reviews and flagging inappropriate content.
"""

from django import forms
from .models import Review, ReviewFlag, Hospital, Doctor

class ReviewForm(forms.ModelForm):
    """
    Form for creating and editing reviews.
    Includes fields for rating different aspects of healthcare service.
    """
    class Meta:
        model = Review
        fields = ['hospital', 'doctor', 'service_quality', 'cost_transparency', 
                 'facility_standards', 'treatment_effectiveness', 'text', 
                 'anonymous', 'patient_id']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        """Initialize form with all available hospitals and doctors"""
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = Doctor.objects.all()
        self.fields['hospital'].queryset = Hospital.objects.all()

class ReviewFlagForm(forms.ModelForm):
    """
    Form for flagging inappropriate reviews.
    Allows users to report problematic content with a reason.
    """
    class Meta:
        model = ReviewFlag
        fields = ['reason']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 3}),
        }