from django.urls import path
from .views import Registration, Login, Profile_update, Dietitian_profile_update
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('registration', Registration, name='registration'),
    path('login', Login.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('profile_update', Profile_update, name='profile_update'),
    path('dietitian_profile_update', Dietitian_profile_update, name='dietitian_profile_update'),
]
