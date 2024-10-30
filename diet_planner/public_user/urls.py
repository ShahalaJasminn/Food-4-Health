from django.urls import path
from .views import Dietitian_specialities, Dietitians, Dietitian_details, personalized_diet_plan, book_consultation, consultation_detail, consultation_list, nutrition_list, nutrition_detail, client_progress, personalized_dietition, user_profile

urlpatterns = [
    path('dietitian_specialities', Dietitian_specialities, name="dietitian_specialities"),
    path('dietitians/<str:speciality>/', Dietitians, name="dietitians"),
    path('dietitian_details/<int:DId>', Dietitian_details, name="dietitian_details"),
    path('diet-plan/', personalized_diet_plan, name="personalized_diet_plan"),
    path('book-consultation/<int:DId>/', book_consultation, name='book_consultation'),
    path('consultation_list/', consultation_list, name='consultation_list'),
    path('consultation_detail/<int:consultation_id>/', consultation_detail, name='consultation_detail'),
    path('nutrition_list/', nutrition_list, name='nutrition_list'),
    path('nutrition_detail/<int:NID>', nutrition_detail, name='nutrition_detail'),
    path('client_progress/', client_progress, name='client_progress'),
    path('personalized_dietition/',personalized_dietition, name='personalized_dietition'),
    path('user_profile/',user_profile, name='user_profile'),
]
