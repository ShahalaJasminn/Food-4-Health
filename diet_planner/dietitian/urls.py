from django.urls import path
from .views import Bookings_and_Consultation, set_availability, consultation_detail_view, chat_screen, list_nutrition_plan, list_clients, client_detail, create_nutrition_plan, nutrition_plan_detail, add_meal_type, edit_nutrition_plan, delete_meal_type, update_client_progress, consultation_list, dietitian_profile, dietitian_availability

urlpatterns = [
    path('appointments', Bookings_and_Consultation, name='appointments'),
    path('set_availability', set_availability, name='set_availability'),
    path('list_consultations', consultation_list, name='list_consultations'),
    path('consultation/<int:consultation_id>/', consultation_detail_view, name='consultation'),
    path('chat/<int:CId>/', chat_screen, name='chat'),
    path("list_clients", list_clients, name="list_clients"),
    path("client_detail/<int:client_id>/",client_detail, name="client_detail"),
    path("update-progress/<int:client_id>/", update_client_progress, name="update_client_progress"),
    path('list_nutrition_plan',list_nutrition_plan, name='list_nutrition_plan'),
    path('nutrition_plan_detail/<int:id>/',nutrition_plan_detail, name='nutrition_plan_detail'),
    path('create_nutrition_plan',create_nutrition_plan, name='create_nutrition_plan'),
    path('add_meal_type/<int:plan_id>/',add_meal_type, name='add_meal_type'),
    path('delete_meal_type/<int:meal_id>/',delete_meal_type, name='delete_meal_type'),
    path('edit_nutrition_plan/<int:plan_id>/',edit_nutrition_plan, name='edit_nutrition_plan'),
    path('dietitian_profile',dietitian_profile, name='dietitian_profile'),
    path('dietitian_availability/<int:id>/',dietitian_availability, name='dietitian_availability'),
]
