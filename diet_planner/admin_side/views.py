from django.shortcuts import render, redirect
from django.http import JsonResponse
from users_account.models import Accounts, Dietitian_Profile

# Create your views here.
def admin_dashboard(req):
    user = req.user
    if user.is_authenticated and user.role == 'admin':
        return redirect('admin_list')
    else:
        return redirect('/')

def DietitianListView(req):
    dietitians = Accounts.objects.filter(role='dietitian').order_by('-id')
    return render(req, 'admin_dietitians_list.html', {'dietitians': dietitians})

def DietitianDetailView(req, id):
    dietitian = Accounts.objects.get(id=id)
    return render(req ,'admin_dietitian_details.html', {'dietitian': dietitian})

def verify_dietitian(request, id):
    if request.method == 'POST':
        dietitian = Dietitian_Profile.objects.get(id=id)
        dietitian.verified = True
        dietitian.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

def users_list(req):
    users = Accounts.objects.filter(role='user')
    return render(req, 'users_list.html', {'users': users})

def users_detail(req, id):
    user = Accounts.objects.get(id=id)
    return render(req, 'user_detail.html', {'user': user})

def block_user(req, id):
    user = Accounts.objects.get(id=id)
    print(user)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()
    return JsonResponse({'status': 'success'})

def admin_list(req):
    admins = Accounts.objects.filter(role='admin').exclude(is_superuser=True)
    return render(req, 'list_admins.html', {'admins': admins})
