from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserType

def index(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            return redirect('dashboard:index')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login:index')
    return render(request, 'login/index.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        user_type = request.POST.get('user_type')

        if not user_type:
            messages.error(request, 'Please select a user type')
            return redirect('login:index')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('login:index')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('login:index')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('login:index')

        user = User.objects.create_user(username=username, email=email, password=password)
        UserType.objects.create(user=user, user_type=user_type)
        auth_login(request, user)
        return redirect('dashboard:index')
    
    return redirect('login:index')

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'You have been logged out successfully')
        return redirect('login:index')
    return redirect('dashboard:index')