from django.shortcuts import render, redirect
from .forms import SignupForm, UserProfileForm, DietitianProfileForm
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from django.http import HttpResponse

# -----------------------------------------------------Pages

def Registration(request):
    role = request.GET.get('role', 'user')
    if request.method == 'POST':
        form = SignupForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)  # Create the user object without saving to the database yet
            
            # Check if the role is admin
            if user.role == 'admin':  # Adjust this condition based on how you define roles
                user.is_active = False  # Disable the account initially
            
            user.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('login')
        else:
            print(form.errors)
            messages.error(request, "Please correct the errors below.")
    else:
        form = SignupForm(initial={'role': role})
    return render(request, 'registration.html', {'form': form})

class Login(LoginView):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        user = request.user  # Access user directly from request
        if user.is_authenticated:  # Check if the user is already logged in
            if user.role == 'user':
                return redirect(reverse_lazy('home'))  # Adjust based on your home URL name
            elif user.role == 'dietitian':
                return redirect(reverse_lazy('dietitian_dashboard'))  # Adjust based on your dietitian URL name
            elif user.role == 'admin':
                return redirect(reverse_lazy('admin_dashboard'))  # Adjust based on your admin URL name
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        user = self.request.user
        if user.role == 'user':
            return reverse_lazy('home')  # Redirect to user home
        elif user.role == 'dietitian':
            return reverse_lazy('dietitian_dashboard')  # Redirect to dietitian dashboard
        elif user.role == 'admin':
            return reverse_lazy('admin_dashboard')  # Redirect to admin dashboard
        return reverse_lazy('landing_page')  # Default redirect if role is unknown

def Profile_update(request):
    profile = request.user.user_profile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'update_profile.html', {'form': form})

def Dietitian_profile_update(request):
    profile = request.user.dietitian_profile

    if request.method == 'POST':
        form = DietitianProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dietitian_dashboard')
    else:
        form = DietitianProfileForm(instance=profile)

    return render(request, 'dietitian_update_profile.html', {'form': form})