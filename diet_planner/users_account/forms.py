import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Accounts, User_Profile, Dietitian_Profile
from django.core import validators, exceptions
from admin_side.models import Specialties, Chronic_conditions


class SignupForm(UserCreationForm):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('dietitian', 'Dietitian'),
        ('admin', 'Admin'),
    ]

    username = forms.CharField(
        max_length=30,
        required=True,
        strip=True,
        validators=[
            validators.RegexValidator(
                regex=r'^[a-zA-Z0-9]*$',
                message="Username must contain at least one alphabet character.",
            ),
        ],
    )
    email = forms.EmailField(required=True)
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
        required=True,
    )
    password2 = forms.CharField(
        label="Confirm Password",
        strip=False,
        widget=forms.PasswordInput,
        required=True,
    )
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        required=True,
        label="Select Account Type",
        widget=forms.HiddenInput(),
    )


    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        if not any(char.isupper() for char in password):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError("Password must contain at least one digit.")
        if not re.search(r'[!@#$%^&*()_+]', password):
            raise forms.ValidationError("Password must contain at least one special character.")
        if len(password) < 8:
            raise forms.ValidationError("Password must contain at least 8 character.")

        return password

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data


    class Meta:
        model = Accounts
        fields = ['username', 'email', 'password1', 'password2', 'role']


class UserProfileForm(forms.ModelForm):
    dietary_goal = forms.ModelMultipleChoiceField(
        queryset=Specialties.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=True
    )
    chronic_condition = forms.ModelMultipleChoiceField(
        queryset=Chronic_conditions.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=True
    )
    
    class Meta:
        model = User_Profile
        fields = [
            'full_name', 'age', 'height', 'weight', 'gender', 'dietary_preference', 
            'photo', 'dietary_goal', 'chronic_condition', 'suger_level', 'cholestrol_level'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control text-capitalize'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'height': forms.NumberInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'dietary_preference': forms.Select(attrs={'class': 'form-select'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'suger_level': forms.NumberInput(attrs={'class': 'form-control'}),
            'cholestrol_level': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class DietitianProfileForm(forms.ModelForm):
    specialties = forms.ModelMultipleChoiceField(
        queryset=Specialties.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False
    )
    class Meta:
        model = Dietitian_Profile
        fields = ['full_name', 'qualifications', 'experience_years', 'specialties', 'certificate', 'bio', 'photo']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control text-capitalize'}),
            'qualifications': forms.TextInput(attrs={'class': 'form-control'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'certificate': forms.FileInput(attrs={'class': 'form-control', 'accept': 'application/pdf'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': '1'}),
            'photo': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }
