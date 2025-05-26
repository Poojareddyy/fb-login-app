from django.shortcuts import render, redirect
from django.contrib.auth import logout

def home(request):
    return render(request, 'core/home.html')

def dashboard(request):
    username = ""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
    return render(request, 'core/dashboard.html', {'username': username})

def logout_view(request):
    logout(request)
    return render(request, 'core/home.html')

