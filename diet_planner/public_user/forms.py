# forms.py
from .models import Message
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from dietitian.models import Consultation, Availability

class ConsultationBookingForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ['date']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
        }

    def __init__(self, *args, dietitian=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.dietitian = dietitian

    def clean_date(self):
        selected_date = self.cleaned_data['date']

        # Ensure time is on the hour
        if selected_date.minute != 0:
            raise ValidationError("Please select a time on the hour (e.g., 10:00, 11:00).")

        # Ensure date is in the future
        if selected_date < timezone.now():
            raise ValidationError("The selected date and time must be in the future.")

        # Check if the dietitian is available on the selected day and time
        availability = Availability.objects.filter(dietitian=self.dietitian).first()
        if not availability:
            raise ValidationError("The dietitian's availability has not been set.")

        if selected_date.strftime('%A').lower() not in availability.get_available_days_list():
            raise ValidationError("The dietitian is not available on the selected day.")

        if not (availability.start_time <= selected_date.time() < availability.end_time):
            raise ValidationError("The selected time is outside the dietitian's available hours.")

        # Ensure no other appointments at the same time
        conflict = Consultation.objects.filter(
            dietitian=self.dietitian,
            date=selected_date
        ).exists()
        if conflict:
            raise ValidationError("This time slot is already booked. Please choose a different time.")

        return selected_date

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Type your message here...', 'class': 'form-control mb-3', 'rows': 1}),
        }