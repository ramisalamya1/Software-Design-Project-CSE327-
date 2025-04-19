from django import forms
from .models import Review, ReviewFlag, Hospital, Doctor


class ReviewForm(forms.ModelForm):
    """
    Form for creating and editing hospital/doctor reviews.
    
    Includes fields for rating different aspects of service,
    adding review text, and optional anonymous posting.
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
        """
        Initialize the form with all available hospitals and doctors.
        """
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = Doctor.objects.all()
        self.fields['hospital'].queryset = Hospital.objects.all()


class ReviewFlagForm(forms.ModelForm):
    """
    Form for flagging inappropriate reviews.
    
    Allows users to submit reasons for reporting a review
    that violates guidelines or contains inappropriate content.
    """

    class Meta:
        model = ReviewFlag
        fields = ['reason']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 3}),
        }