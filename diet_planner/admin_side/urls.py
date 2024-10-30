from django.urls import path
from .views import admin_dashboard, DietitianListView, DietitianDetailView, verify_dietitian, users_list, users_detail, block_user, admin_list

urlpatterns = [
    path('', admin_dashboard, name="admin_dashboard"),
    path('dietitians/', DietitianListView, name='dietitian_list'),
    path('admin_dietitian/<int:id>/', DietitianDetailView, name='admin_dietitian_detail'),
    path('verify-dietitian/<int:id>/', verify_dietitian, name='verify_dietitian'),
    path('users', users_list, name="users_list"),
    path('user/<int:id>/', users_detail, name='user_detail'),
    path('block_user/<int:id>/', block_user, name='block_user'),
    path('admin_list', admin_list, name='admin_list'),
]
