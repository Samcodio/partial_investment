from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .form import *

# Create your views here.


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('form_app:home')
        else:
            messages.error(request, 'Invalid details')
    context = {}
    return render(request, 'authenticate/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('user_login:login')


def registration(request):
    form = RegistrationForm()  # Initialize form outside the if block
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! An OTP has been sent to your email")
            return redirect('form_app:verify_email', username=request.POST['username'])
    else:
        messages.error(request, 'Invalid details')
    context = {
        'form': form
    }
    return render(request, 'authenticate/registration.html', context)

