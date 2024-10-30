from django.contrib import admin
from .models import Accounts, User_Profile, Dietitian_Profile

class User_account(admin.ModelAdmin):
    list_display = ['username', 'email', 'role', 'is_active']
    list_editable = ['email', 'is_active', 'role']

class User_profile(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'dietary_preference']
    list_editable = ['dietary_preference']

class Dietitian_profile(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'verified']
    list_editable = ['verified']

admin.site.register(Accounts, User_account)
admin.site.register(User_Profile, User_profile)
admin.site.register(Dietitian_Profile, Dietitian_profile)