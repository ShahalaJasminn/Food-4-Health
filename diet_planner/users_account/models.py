from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from admin_side.models import Specialties, Chronic_conditions

# Choices
ROLE_CHOICE = [
    ('dietitian', 'DIETITIAN'),
    ('user', 'USER'),
    ('admin', 'ADMIN'),
]

GENDER_CHOICE = [
    ('male', 'MALE'),
    ('female', 'FEMALE'),
    ('other', 'PREFER NOT TO SAY'),
]

DIETARY_PREFERENCE_CHOICES = [
    ('Vegetarian', 'Vegetarian'),
    ('Vegan', 'Vegan'),
    ('Keto', 'Keto'),
    ('Paleo', 'Paleo'),
    ('Gluten-Free', 'Gluten-Free'),
    ('None', 'No Preference'),
]

# Accounts Model
class Accounts(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=55, unique=True)
    role = models.CharField(choices=ROLE_CHOICE, default='user', max_length=100)
    
    def __str__(self):
        return self.username
    
    @property
    def is_profile_complete(self):
        if self.role == 'user' and hasattr(self, 'user_profile'):
            return self.user_profile.is_profile_complete()
        elif self.role == 'dietitian' and hasattr(self, 'dietitian_profile'):
            return self.dietitian_profile.is_profile_complete()
        return False  # If no matching role or profile exists

# User Profile Model
class User_Profile(models.Model):
    user = models.OneToOneField(Accounts, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, null=False, blank=False)
    photo = models.ImageField(upload_to='profile_photos', default='assets/profile.png')
    age = models.PositiveIntegerField(null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    gender = models.CharField(choices=GENDER_CHOICE, max_length=100, blank=True, null=True)
    dietary_preference = models.CharField(choices=DIETARY_PREFERENCE_CHOICES, max_length=50, default='None')
    dietary_goal = models.ManyToManyField(Specialties)
    chronic_condition = models.ManyToManyField(Chronic_conditions)
    suger_level = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    cholestrol_level = models.DecimalField(max_digits=5, decimal_places=2, default=0)


    def __str__(self):
        return self.user.username

    def is_profile_complete(self):
        mandatory_fields = [self.full_name, self.age, self.weight, self.height, self.gender]
        return all(mandatory_fields)

# Dietitian Profile Model
class Dietitian_Profile(models.Model):
    user = models.OneToOneField(Accounts, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, null=False, blank=False)
    photo = models.ImageField(upload_to='dietitian_photos', default='assets/profile.png')
    qualifications = models.TextField(null=False, blank=False)
    experience_years = models.PositiveIntegerField(null=True, blank=True)
    specialties = models.ManyToManyField(Specialties)
    certificate = models.FileField(upload_to="dietitian_certificates",null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    available = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name} - {self.user.username}"

    def is_profile_complete(self):
        mandatory_fields = [self.full_name, self.qualifications, self.experience_years, self.certificate]
        return all(mandatory_fields)

# Signals for profile creation
@receiver(post_save, sender=Accounts)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'user':
            User_Profile.objects.create(user=instance)
        elif instance.role == 'dietitian':
            Dietitian_Profile.objects.create(user=instance)

@receiver(post_save, sender=Accounts)
def save_profile(sender, instance, **kwargs):
    if instance.role == 'user' and hasattr(instance, 'user_profile'):
        instance.user_profile.save()
    elif instance.role == 'dietitian' and hasattr(instance, 'dietitian_profile'):
        instance.dietitian_profile.save()
