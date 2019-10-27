from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')

    user = request.POST.get('user')
    password = request.POST.get('password')

    user = auth.authenticate(
        request,
        username=user,
        password=password
    )

    if not user:
        messages.error(request, 'Username or password is invalid')
        return render(request, 'accounts/login.html')
    else:
        auth.login(request, user)
        messages.success(request, 'Login successfully')
        return redirect('dashboard')

def logout(request):
    auth.logout(request)
    return redirect('login')

def register(request):
    if request.method != 'POST':
        return render(request, 'accounts/register.html')

    name = request.POST.get('name')
    last_name = request.POST.get('last_name')
    user = request.POST.get('user')
    email = request.POST.get('email')
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirm_password')

    fields = [name, last_name, email, password, confirm_password]
    empty_fields = [field for field in fields if not field]

    if len(empty_fields) > 0:
        messages.error(request, 'Fill in all required fields')
        return render(request, 'accounts/register.html')

    try:
        validate_email(email)
    except:
        messages.error(request, 'Invalid email')
        return render(request, 'accounts/register.html')

    if len(user) < 6:
        messages.error(request, 'User must be at least 6 characters')
        return render(request, 'accounts/register.html')

    if len(password) < 6:
        messages.error(request, 'Password must be at least 6 characters')
        return render(request, 'accounts/register.html')

    if password != confirm_password:
        messages.error(request, 'Password confirmation doesn\'t match password')
        return render(request, 'accounts/register.html')

    if User.objects.filter(username=user).exists():
        messages.error(request, 'User already exists')
        return render(request, 'accounts/register.html')

    if User.objects.filter(email=email).exists():
        messages.error(request, 'Email already exists')
        return render(request, 'accounts/register.html')

    messages.success(request, 'Successfully registered')
    
    user = User.objects.create_user(
        username=user,
        email=email,
        password=password,
        first_name=name,
        last_name=last_name
    )

    user.save()

    return redirect('login')

@login_required(redirect_field_name='login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')
