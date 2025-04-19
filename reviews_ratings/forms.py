from django import forms
from django.core.validators import MinLengthValidator
from .models import Review, ReviewFlag, Hospital, Doctor


class ReviewForm(forms.ModelForm):
    """
    Form for creating and editing hospital/doctor reviews.
    
    Includes fields for rating different aspects of service,
    adding review text, and optional anonymous posting.
    """
    
    text = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 4,
            'placeholder': 'Share your experience...',
            'class': 'form-control'
        }),
        validators=[MinLengthValidator(10, 'Review must be at least 10 characters long')],
        help_text='Provide detailed feedback about your experience'
    )

    class Meta:
        model = Review
        fields = [
            'hospital', 'doctor', 'service_quality', 'cost_transparency',
            'facility_standards', 'treatment_effectiveness', 'text',
            'anonymous', 'patient_id'
        ]
        widgets = {
            'hospital': forms.Select(attrs={'class': 'form-select'}),
            'doctor': forms.Select(attrs={'class': 'form-select'}),
            'service_quality': forms.Select(attrs={'class': 'form-select'}),
            'cost_transparency': forms.Select(attrs={'class': 'form-select'}),
            'facility_standards': forms.Select(attrs={'class': 'form-select'}),
            'treatment_effectiveness': forms.Select(attrs={'class': 'form-select'}),
            'patient_id': forms.TextInput(attrs={'class': 'form-control'}),
            'anonymous': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize the form with all available hospitals and doctors.
        Add custom labels and help texts.
        """
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = Doctor.objects.all().order_by('name')
        self.fields['hospital'].queryset = Hospital.objects.all().order_by('name')
        
        # Custom labels
        self.fields['service_quality'].label = 'Quality of Service'
        self.fields['cost_transparency'].label = 'Cost Transparency'
        self.fields['facility_standards'].label = 'Facility Standards'
        self.fields['treatment_effectiveness'].label = 'Treatment Effectiveness'
        
        # Help texts
        self.fields['anonymous'].help_text = 'Check this if you want to hide your identity'
        self.fields['patient_id'].help_text = 'Your unique patient identifier'

    def clean(self):
        """
        Custom validation to ensure either hospital or doctor is selected.
        """
        cleaned_data = super().clean()
        hospital = cleaned_data.get('hospital')
        doctor = cleaned_data.get('doctor')

        if not hospital and not doctor:
            raise forms.ValidationError(
                "Please select either a hospital or a doctor for your review"
            )

        return cleaned_data


class ReviewFlagForm(forms.ModelForm):
    """
    Form for flagging inappropriate reviews.
    
    Allows users to submit reasons for reporting a review
    that violates guidelines or contains inappropriate content.
    """

    reason = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Please explain why this review should be flagged...',
            'class': 'form-control'
        }),
        validators=[MinLengthValidator(20, 'Please provide a detailed explanation (at least 20 characters)')],
        help_text='Describe the issue with this review in detail'
    )

    class Meta:
        model = ReviewFlag
        fields = ['reason']

    def clean_reason(self):
        """
        Additional validation for the reason field.
        """
        reason = self.cleaned_data.get('reason')
        if reason and reason.lower().strip() == 'spam':
            raise forms.ValidationError(
                "Please provide a more detailed explanation than just 'spam'"
            )
        return reason