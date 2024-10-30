from django.shortcuts import render, redirect
from users_account.models import Accounts
from dietitian.models import Consultation, NutritionPlan, ClientProgress
from django.utils import timezone

# Create your views here.
def Landing(request):
    return render(request, "home.html")

def Home(request):
    user = request.user
    if user.is_authenticated and user.role == 'user':
        return render(request, "user_home.html")
    return redirect('/')

def Dietitian_dashboard(request):
    user = request.user
    if user.is_authenticated and user.role == 'dietitian':
        now = timezone.now()
        appointment_count = Consultation.objects.filter(dietitian=user, confirmed=True).count()
        nutrition_plan_count = NutritionPlan.objects.filter(dietitian=user).count()
        client_count = ClientProgress.objects.filter(dietitian=user).count()
        client_progress = ClientProgress.objects.filter(dietitian=user)
        total_progress = sum(client.progress for client in client_progress)
        goal_progress = (total_progress / (client_count * 100)) * 100 if client_count > 0 else 0

        client_names = [client.client.user_profile.full_name for client in client_progress]
        client_progress_values = [float(client.progress) for client in client_progress]

        recent_consultation = Consultation.objects.filter(dietitian=user, confirmed=True, date__lte=now)
        context = {
            'client_count': client_count,
            "appointment_count": appointment_count,
            'nutrition_plan_count': nutrition_plan_count,
            'goal_progress': goal_progress,
            'client_names': client_names,
            'client_progress_values': client_progress_values,
            'recent_consultation': recent_consultation
        }
        return render(request, 'dietitian_dashboard.html', context)
    return redirect('/')
    