from django import forms
from .models import Review, ReviewFlag, Hospital, Doctor

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['hospital', 'doctor', 'service_quality', 'cost_transparency', 
                 'facility_standards', 'treatment_effectiveness', 'text', 
                 'anonymous', 'patient_id']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = Doctor.objects.all()
        self.fields['hospital'].queryset = Hospital.objects.all()

class ReviewFlagForm(forms.ModelForm):
    class Meta:
        model = ReviewFlag
        fields = ['reason']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 3}),
        }