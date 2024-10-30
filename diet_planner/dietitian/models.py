from django.db import models
from users_account.models import Accounts
from django.core.exceptions import ValidationError

# Create your models here.
class Availability(models.Model):
    DAYS_OF_THE_WEEK = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]
    dietitian = models.ForeignKey(Accounts, on_delete=models.CASCADE, related_name='availabilities')
    available_days = models.TextField(blank=True, default="")
    start_time = models.TimeField()
    end_time = models.TimeField()

    def save(self, *args, **kwargs):
        if self.start_time >= self.end_time:
            raise ValidationError("End time must be after start time.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.dietitian.username} available on {self.available_days} from {self.start_time} to {self.end_time}"
    
    # Helper method to get available days as a list
    def get_available_days_list(self):
        return self.available_days.split(',') if self.available_days else []

    # Helper method to set available days from a list
    def set_available_days_list(self, days_list):
        self.available_days = ','.join(days_list)


class Consultation(models.Model):
    dietitian = models.ForeignKey(Accounts, on_delete=models.CASCADE, related_name='dietitian_consultations')
    client = models.ForeignKey(Accounts, on_delete=models.CASCADE, related_name='client_consultations')
    date = models.DateTimeField()
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Consultation with {self.client} on {self.date}"
    
class ClientProgress(models.Model):
    client = models.ForeignKey(Accounts, on_delete=models.CASCADE, related_name='progress_records')
    dietitian = models.ForeignKey(Accounts, on_delete=models.CASCADE, related_name='progress_updates')
    progress = models.DecimalField(max_digits=5, decimal_places=2)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Progress for {self.client} on {self.date_updated}: {self.progress}%"
 

class NutritionPlan(models.Model):
    dietitian = models.ForeignKey(Accounts, on_delete=models.CASCADE, related_name='created_plans')
    client = models.ForeignKey(Accounts, on_delete=models.CASCADE, related_name='nutrition_plans')
    plan_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, help_text="Brief description of the plan")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.plan_name} for {self.client.username}"


class MealType(models.Model):
    name = models.CharField(max_length=255)
    nutrition_plan = models.ForeignKey(NutritionPlan, related_name='meal_types', on_delete=models.CASCADE)
    calories = models.FloatField(null=True, blank=True)
    fat = models.FloatField(null=True, blank=True)
    cholesterol = models.FloatField(null=True, blank=True)
    protein = models.FloatField(null=True, blank=True)
    carbohydrates = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

