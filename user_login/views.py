from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .form import *

# Create your views here.


# def dashboard(request):
#     return render(request, 'Users/dashboard.html')


# def signUp(request):
#     return render(request, 'Authentications/register.html')


# def sigIn(request):
#     return render(request, 'Authentications/login.html')


# def otpVerify(request):
#     return render(request, 'Authentications/otpVerify.html')


# def userList(request):
#     return render(request, 'Admin/userList.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('form_app:home')
        else:
            messages.info(request, 'Invalid details')
    context = {}
    return render(request, 'Authentications/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('form_app:home')


def otpmessage(request):
    context = {}
    return render(request, 'Authentications/otpmessage.html', context)


def registration(request):
    form = RegistrationForm()  # Initialize form outside the if block
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_login:otpmessage')
    else:
        messages.error(request, 'Invalid details')
    context = {
        'form': form
    }
    return render(request, 'Authentications/register.html', context)

