from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

class CheckProfileCompleteMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        
        exempt_paths = [
            reverse('login'),
            reverse('landing_page'),
            reverse('registration'),
            reverse('logout'),
            reverse('profile_update'),
            reverse('dietitian_profile_update'),
            reverse('admin:index'),
        ]

        exempt_admin = [
            '/admin/',
            '/media/',
            '/administration/'
        ]

        if request.path in exempt_paths or any(request.path.startswith(exempt) for exempt in exempt_admin):
            return self.get_response(request)

        if user.is_authenticated:
            if not user.is_profile_complete:
                print(user.is_profile_complete, user.role)
                if user.role == 'user':
                    return redirect('profile_update')
                elif user.role == 'dietitian':
                    return redirect('dietitian_profile_update')

        response = self.get_response(request)
        return response


class CheckLogged:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        exempt_paths = [
            reverse('login'),
            reverse('landing_page'),
            reverse('registration'),
            reverse('logout'),
            reverse('admin:index'),
        ]

        if request.path in exempt_paths or request.path.startswith('/admin'):
            return self.get_response(request)

        if not user.is_authenticated:
            return redirect('/')
        
        response = self.get_response(request)
        return response
    

class DietitianVerification:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        exempt_paths = [
            reverse('login'),
            reverse('registration'),
            reverse('logout'),
            reverse('dietitian_profile_update'),
            reverse('dietitian_dashboard'),
            reverse('admin:index'),
        ]

        exempt_admin = [
            '/admin/',
            '/media/',
            '/administration/'
        ]

        if request.path in exempt_paths or any(request.path.startswith(exempt) for exempt in exempt_admin):
            return self.get_response(request)
        
        if user.is_authenticated and user.role == 'dietitian':
            dietitian_profile = getattr(user, 'dietitian_profile', None)
            if dietitian_profile and not dietitian_profile.verified:
                # Show a message to the user
                messages.warning(request, "Your profile isn't verified by admin.")
                # Redirect to the dashboard
                return redirect('dietitian_dashboard')
        
        response = self.get_response(request)
        return response