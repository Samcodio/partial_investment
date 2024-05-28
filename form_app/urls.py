from django.urls import path
from . import views

app_name = 'form_app'


urlpatterns = [
    path('', views.home, name='home'),
    path('user_profile', views.profile_page, name='user_profile'),
    path('listed-jobs/', views.list_pdf, name='list_pdf'),
    path('post_pdf', views.post_pdf, name='post_pdf'),
    path('details/<int:pk>', views.pdf_details, name='pdf_details'),
    path('verify-email/<str:username>', views.verify_email, name='verify_email'),
    path('resend_email/', views.resend_otp, name='resend_email'),
]

