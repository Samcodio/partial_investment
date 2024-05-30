from django.urls import path
from . import views

app_name = 'form_app'


urlpatterns = [
    path('', views.home, name='home'),
    path('user_profile', views.profile_page, name='user_profile'),
    path('edit-profile', views.edit_profile, name='edit_profile'),
    path('list_of-users/', views.list_users, name='list_users'),
    path('listed-jobs/', views.list_pdf, name='list_pdf'),
    path('post_pdf', views.post_pdf, name='post_pdf'),
    path('details/<int:pk>', views.pdf_details, name='pdf_details'),
    path('verify-email/<str:username>', views.verify_email, name='verify_email'),
    path('resend_email/', views.resend_otp, name='resend_email'),
    path('withdrawal-page/<int:pk>', views.user_amnt, name='user_amount'),
    path('adjust-_-amount/<int:pk>', views.adjust_amount, name='adjust_amount'),
]

