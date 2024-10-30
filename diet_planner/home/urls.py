from django.urls import path
from .views import Landing ,Home, Dietitian_dashboard

urlpatterns = [
    path('', Landing, name="landing_page"),
    path('home', Home, name="home"),
    path('dietitian_dashboard', Dietitian_dashboard, name="dietitian_dashboard"),
]
