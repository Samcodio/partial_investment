from django.urls import path
from . import views

app_name = 'user_login'

urlpatterns = [
    path('Dashboard/', views.dashboard, name='dashboard'),
    path('signUp/', views.signUp, name='signUp'),
    path('signIn/', views.sigIn, name='signIn'),
    path('otpVerify/', views.otpVerify, name='otpVerify'),

    # path('log-user/', views.login_user, name='login'),
    # path('logout_user/', views.logout_user, name='logout'),
    # path('reg-user/', views.registration, name='registration'),
]

