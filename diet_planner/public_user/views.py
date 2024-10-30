from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from users_account.models import Accounts, User_Profile
from dietitian.models import Availability, Consultation, NutritionPlan, ClientProgress
from .utils import fetch_diet_plan
from .forms import ConsultationBookingForm, MessageForm
from admin_side.models import Specialties


# Create your views here.
def Dietitian_specialities(req):
    specialities = Specialties.objects.all()
    return render(req, "dietitian_plan.html", {'specialities': specialities})

def Dietitians(req, speciality):
    dietitians = Accounts.objects.filter(role='dietitian', dietitian_profile__specialties__name__icontains=speciality).exclude(dietitian_profile__verified=False)
    return render(req, "dietitian_list.html", {'dietitians': dietitians})

def Dietitian_details(req, DId):
    dietitian = Accounts.objects.get(id=DId)
    try:
        availability = Availability.objects.get(dietitian=dietitian)
    except Availability.DoesNotExist:
        availability = None

    specialty = dietitian.dietitian_profile.specialties
    

    return render(req, 'dietitian_details.html', {
        'dietitian': dietitian,
        'availability': availability,
        'specialties': specialty,
    })

def personalized_diet_plan(request):
    user_profile = User_Profile.objects.get(user=request.user)
    weight = user_profile.weight
    height = user_profile.height
    dietary_preference = user_profile.dietary_preference  # e.g., 'vegan', 'low carb'
    sugar_level = user_profile.suger_level
    cholesterol_level = user_profile.cholestrol_level

    suggested_plan = fetch_diet_plan(weight, height, dietary_preference, sugar_level, cholesterol_level)
    
    return render(request, 'personalized_diet_plan.html', {
        'suggested_plan': suggested_plan,
        'user_profile': user_profile,
    })

def book_consultation(request, DId):
    dietitian = get_object_or_404(Accounts, id=DId)

    if request.method == 'POST':
        form = ConsultationBookingForm(request.POST, dietitian=dietitian)
        if form.is_valid():
            consultation = form.save(commit=False)
            consultation.dietitian = dietitian
            consultation.client = request.user
            consultation.save()
            messages.success(request, "Your consultation has been booked successfully.")
            return redirect('dietitian_details', DId=dietitian.id)
    else:
        form = ConsultationBookingForm(dietitian=dietitian)

    return render(request, 'book_consultation.html', {
        'dietitian': dietitian,
        'form': form,
    })

def consultation_list(request):
    consultations = Consultation.objects.filter(client=request.user).select_related('dietitian').order_by('-date')
    return render(request, 'consultation_list.html', {'consultations': consultations})

def consultation_detail(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id, client=request.user)
    messages_list = consultation.messages.order_by('timestamp')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.consultation = consultation
            new_message.sender = request.user
            new_message.save()
            return redirect('consultation_detail', consultation_id=consultation_id)
    else:
        form = MessageForm()

    return render(request, 'consultation_detail.html', {
        'consultation': consultation,
        'messages_list': messages_list,
        'form': form
    })

def nutrition_list(req):
    nutrition_plans = NutritionPlan.objects.filter(client=req.user)
    return render(req, 'nutrition_list.html', {
        'nutrition_plans': nutrition_plans,
    })

def nutrition_detail(req, NID):
    nutrition_plan = NutritionPlan.objects.get(id=NID)
    return render(req, 'nutrition_detail.html', {
        'nutrition_plan': nutrition_plan,
    })

def client_progress(req):
    progress_records = ClientProgress.objects.filter(client=req.user)
    return render(req, 'client_progress.html', {
        'progress_records': progress_records,
    })

def personalized_dietition(req):
    user_goals = req.user.user_profile.dietary_goal.all()  
    dietitians = Accounts.objects.filter(
        role='dietitian', 
        dietitian_profile__specialties__in=user_goals
    ).distinct()
    return render(req, 'personalized_dietitian.html', {
        'dietitians': dietitians,
    })

def user_profile(request):
    print("Reached")
    user_profile = get_object_or_404(User_Profile, user=request.user)
    return render(request, 'user_profile.html', {
        'user_profile': user_profile,
    })
