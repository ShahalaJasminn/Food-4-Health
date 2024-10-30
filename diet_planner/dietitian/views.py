from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import MultiDayAvailabilityForm, ConsultationUpdateForm, NutritionPlanForm, MealTypeForm, UpdateProgressForm
from .models import Availability, Consultation, NutritionPlan, MealType, ClientProgress
from users_account.models import Accounts, Dietitian_Profile
from django.utils import timezone
from django.http import JsonResponse
from .utils import fetch_nutrition_details_from_nutritionix
from datetime import timedelta
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Q

def Bookings_and_Consultation(request):
    # Check all consultation bookings
    consultations_booked = Consultation.objects.filter(dietitian=request.user, confirmed=False).order_by('-id')

    # Consultations that are fully finished before now
    consultations_finished = Consultation.objects.filter(
        dietitian=request.user,
        confirmed=True,
        date__lt=timezone.now() - timedelta(hours=1)
    ).order_by('-id')

    availability = Availability.objects.filter(dietitian=request.user).first()
    return render(request, 'appointments.html', {
        'availability': availability,
        'consultations_booked': consultations_booked,
        'consultations_finished': consultations_finished,
    })


def set_availability(request):
    availability, created = Availability.objects.get_or_create(
        dietitian=request.user,
        defaults={'start_time': '09:00', 'end_time': '17:00'}
    )

    if request.method == 'POST':
        form = MultiDayAvailabilityForm(request.POST, availability=availability)
        if form.is_valid():
            # Save selected days, start time, and end time
            selected_days = form.cleaned_data['available_days']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']

            availability.set_available_days_list(selected_days)
            availability.start_time = start_time
            availability.end_time = end_time
            availability.save()
            
            return redirect('appointments')
    else:
        form = MultiDayAvailabilityForm(availability=availability)

    return render(request, 'set_availability.html', {'form': form})


def consultation_detail_view(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id)

    if request.method == "POST":
        form = ConsultationUpdateForm(request.POST, instance=consultation)
        if form.is_valid():
            form.save()
            messages.success(request, "Consultation updated successfully.")
            return redirect('consultation', consultation_id=consultation.id)
    else:
        form = ConsultationUpdateForm(instance=consultation)

    return render(request, 'consultation_detail_view.html', {
        'consultation': consultation,
        'form': form,
    })


def consultation_list(req):
    now = timezone.now()
    end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=999999)
    consultations_pending = Consultation.objects.filter(
        dietitian=req.user,
        confirmed=True,
        date__gte=now - timedelta(hours=1)   # For ongoing (started within last hour)
    ).order_by('date')
    return render(req, 'consultations_list.html', {
        'consultations_pending': consultations_pending,
    })

def chat_screen(request, CId):
    consultation = Consultation.objects.get(id=CId)
    messages_list = consultation.messages.order_by('timestamp')
    print(consultation)
    return render(request, 'chat_screen.html', {'consultation': consultation, 'messages_list': messages_list})


def list_clients(request):
    now = timezone.now()
    end_of_today = now.replace(hour=23, minute=59, second=59, microsecond=999999)
    consultations = Consultation.objects.filter(
        dietitian=request.user,
        confirmed=True,
        date__lte=end_of_today
    ).values('client').distinct()
    client_ids = [client['client'] for client in consultations]
    unique_clients = Accounts.objects.filter(id__in=client_ids)

    return render(request, "list_clients.html", {'clients': unique_clients})


def client_detail(request, client_id):
    now = timezone.now()
    end_of_today = now.replace(hour=23, minute=59, second=59, microsecond=999999)

    client = get_object_or_404(Accounts, id=client_id)
    consultations = Consultation.objects.filter(
        client=client, dietitian=request.user, confirmed=True, date__lte=end_of_today
    ).order_by('-date')

    existing_progress = ClientProgress.objects.filter(dietitian=request.user, client=client_id).first()

    form = UpdateProgressForm()

    return render(request, "client_detail.html", {
        'client': client,
        'consultations': consultations,
        'progress': existing_progress,
        'form': form,
    })


@csrf_exempt
def update_client_progress(request, client_id):
    if request.method == "POST":
        client = get_object_or_404(Accounts, id=client_id)
        dietitian = request.user
        data = json.loads(request.body)
        progress = data.get("progress")

        client_progress, created = ClientProgress.objects.update_or_create(
            dietitian=dietitian, client=client,
            defaults={'progress': progress}
        )

        return JsonResponse({"success": True, "new_progress": client_progress.progress})

    return JsonResponse({"success": False}, status=400)


def list_nutrition_plan(request):
    nutrition_plans = NutritionPlan.objects.filter(dietitian=request.user)
    return render(request, "list_nutrition_plan.html", {'nutrition_plans': nutrition_plans})


def create_nutrition_plan(request):
    client_id = request.GET.get('client')
    if request.method == 'POST':
        nutrition_plan_form = NutritionPlanForm(request.POST)
        if nutrition_plan_form.is_valid():
            client = nutrition_plan_form.cleaned_data['client']
            if NutritionPlan.objects.filter(client=client).exists():
                messages.error(request, "This client already has an active nutrition plan.")
                return redirect('list_nutrition_plan')
            nutrition_plan = nutrition_plan_form.save()
            return redirect('nutrition_plan_detail', nutrition_plan.id)
    else:
        nutrition_plan_form = NutritionPlanForm(initial={'client': client_id, 'dietitian': request.user})
    return render(request, 'create_nutrition_plan.html', {'form': nutrition_plan_form})


def nutrition_plan_detail(request, id):
    nutrition_plan = get_object_or_404(NutritionPlan, id=id)
    meal_type_form = MealTypeForm()
    return render(request, 'nutrition_plan_detail.html', {
        'nutrition_plan': nutrition_plan,
        'meal_type_form': meal_type_form
    })


def add_meal_type(request, plan_id):
    if request.method == 'POST':
        meal_form = MealTypeForm(request.POST)
        nutrition_plan = get_object_or_404(NutritionPlan, id=plan_id)
        
        if meal_form.is_valid():
            meal = meal_form.save(commit=False)
            meal.nutrition_plan = nutrition_plan
            meal.save()
            
            # Fetch meal details from Nutritionix
            meal_details = fetch_nutrition_details_from_nutritionix(meal.name)
            if meal_details:
                # Update meal with fetched details
                meal.calories = meal_details['calories']
                meal.fat = meal_details['fat']
                meal.cholesterol = meal_details['cholesterol']
                meal.protein = meal_details['protein']
                meal.carbohydrates = meal_details['carbohydrates']
                meal.save()

            # For AJAX request, return JSON response
            return JsonResponse({
                'meal': {
                    'name': meal.name,
                    'calories': meal.calories,
                    'fat': meal.fat,
                    'cholesterol': meal.cholesterol,
                    'protein': meal.protein,
                    'carbohydrates': meal.carbohydrates
                }
            })
        else:
            return JsonResponse({'errors': meal_form.errors}, status=400)
    return redirect('nutrition_plan_detail', plan_id)


def delete_meal_type(request, meal_id):
    try:
        meal = MealType.objects.get(id=meal_id)
        meal.delete()
        return JsonResponse({'success': True})
    except MealType.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Meal type not found'})


def edit_nutrition_plan(request, plan_id):
    nutrition_plan = NutritionPlan.objects.get(id=plan_id)

    if request.method == 'POST':
        nutrition_plan_form = NutritionPlanForm(request.POST, instance=nutrition_plan)
        if nutrition_plan_form.is_valid():
            nutrition_plan_form.save()  # Save any adjustments to the nutrition plan
            return redirect('nutrition_plan_detail', nutrition_plan.id)
    else:
        nutrition_plan_form = NutritionPlanForm(instance=nutrition_plan)

    return render(request, 'edit_nutrition_plan.html', {
        'form': nutrition_plan_form,
    })

def dietitian_profile(request):
    dietitian_profile = get_object_or_404(Dietitian_Profile, user=request.user)
    availability = Availability.objects.filter(dietitian=request.user).first()
    return render(request, 'dietitian_profile.html', {
        'dietitian_profile': dietitian_profile,
        'availability': availability
    })

def dietitian_availability(request, id):
    if request.method == 'POST':
        dietitian = Dietitian_Profile.objects.get(id=id)
        if dietitian.available:
            dietitian.available = False
        else:
            dietitian.available = True
        dietitian.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)