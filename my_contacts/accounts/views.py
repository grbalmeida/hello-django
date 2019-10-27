from django.shortcuts import render
from django.contrib import messages

def login(request):
    return render(request, 'accounts/login.html')

def logout(request):
    pass

def register(request):
    return render(request, 'accounts/register.html')

def dashboard(request):
    return render(request, 'accounts/dashboard.html')
