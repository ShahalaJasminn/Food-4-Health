from django import forms
from .models import Consultation, NutritionPlan, MealType

class MultiDayAvailabilityForm(forms.Form):
    DAYS_OF_THE_WEEK = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]

    available_days = forms.MultipleChoiceField(
        choices=DAYS_OF_THE_WEEK,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check'}),
        required=True,
        label="Select Available Days"
    )
    start_time = forms.TimeField(
        required=True,
        label="Start Time",
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'})
    )
    end_time = forms.TimeField(
        required=True,
        label="End Time",
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        # Accept an 'availability' instance to pre-fill the form if it exists
        availability = kwargs.pop('availability', None)
        super().__init__(*args, **kwargs)
        
        if availability:
            # Pre-fill available days as a list of selected days
            self.fields['available_days'].initial = availability.get_available_days_list()
            self.fields['start_time'].initial = availability.start_time
            self.fields['end_time'].initial = availability.end_time

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        # Only perform the time comparison if both start_time and end_time are provided
        if start_time and end_time:
            if start_time >= end_time:
                raise forms.ValidationError("End time must be after start time.")
        return cleaned_data


class ConsultationUpdateForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ['confirmed']  # Add any fields you want to allow for updating

    def clean_date(self):
        date = self.cleaned_data['date']
        # Add any custom validation for the date here if needed
        return date


class NutritionPlanForm(forms.ModelForm):
    class Meta:
        model = NutritionPlan
        fields = ['client', 'dietitian', 'plan_name', 'description']
        widgets = {
            'client': forms.HiddenInput(),
            'dietitian': forms.HiddenInput()
        }


class MealTypeForm(forms.ModelForm):
    class Meta:
        model = MealType
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }


class UpdateProgressForm(forms.Form):
    progress = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        label="Progress (%)",
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        help_text="Enter the client's progress as a percentage."
    )