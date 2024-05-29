from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone
# Create your views here.


def home(request):
    context = {}
    return render(request, 'form_app/index.html', context)


def list_pdf(request):
    # get_pdf = get_object_or_404(Post_pdf)
    posts = Post_pdf.objects.all()
    # pdf_part = get_pdf.pdf_file
    # response = HttpResponse(pdf_part.read(), content_type='application/pdf')
    # return response
    count = posts.count()
    context = {
        'posts': posts,
        'count': count
    }
    return render(request, 'form_app/Posts/pdf.html', context)


def post_pdf(request):
    form = post_form()
    if request.method == 'POST':
        form = post_form(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('form_app:list_pdf')
        else:
            messages.error(request, 'Invalid details')
    context = {
        'form': form
    }
    return render(request, 'form_app/Posts/create_post.html', context)


def pdf_details(request, pk):
    pdfdetails = get_object_or_404(Post_pdf, pk=pk)
    pdf_page = pdfdetails.pdf_file
    response = HttpResponse(pdf_page.read(), content_type='application/pdf')
    return response
    if request.method == 'POST':
        pdfdetails.delete()
        return redirect('form_app:list_pdf')
    context = {
        'pdfdetails': pdfdetails
    }
    return render(request, 'form_app/Posts/details.html', context)


def verify_email(request, username):
    user = CustomUser.objects.get(username=username)
    user_otp = Otptoken.objects.filter(user=user).last()
    if request.method == 'POST':
        if user_otp.otp_code == request.POST['otp_code']:

            #not expired
            if user_otp.otp_expires_at > timezone.now():
                user.is_active = True
                user.save()
                messages.success(request, "Account successfully created")
                return redirect("user_login:login")
            #expired
            else:
                messages.warning(request, "This OTP has expired, please get a new OTP")
                return redirect('form_app:verify_email', username=user.username)

        #invalid otp
        else:
            messages.warning(request, "Invalid OTP entered")
            return redirect('form_app:verify_email', username=user.username)
    context = {}
    return render(request, 'form_app/Verification/verify.html', context)


def resend_otp(request):
    if request.method == 'POST':
        user_email = request.POST["otp_email"]

        if CustomUser.objects.filter(email=user_email).exists():
            user = CustomUser.objects.get(email=user_email)
            otp = Otptoken.objects.create(user=user, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))

#             email variables
            subject = "Email Verification"
            message = f"""
                                    Hello, {user.username}
                                    Your OTP is {otp.otp_code}
                                    It expires in 5 minutes. Use the link to return to the webpage\n
                                    http://1270.0.0.1.8000/verify-email/{user.username}
                            """
            sender = "nosikesamuel1@gmail.com"
            receiver = [user.email, ]

            # send email
            send_mail(
                subject,
                message,
                sender,
                receiver,
                fail_silently=False
            )
            messages.success(request, 'A new otp has been sent to your email address')
            return redirect('form_app:verify_email', username=user.username)
        else:
            messages.warning(request, 'PLease enter the email used')
            return redirect('form_app:resend_email')
    context = {}
    return render(request, 'form_app/Verification/resend.html', context)


def profile_page(request):
    userdetails = request.user
    context = {
        'userdetails': userdetails
    }
    return render(request, 'form_app/profile.html', context)


def edit_profile(request):
    profileform = EditProfileInfo(instance=request.user)
    if request.method == 'POST':
        profileform = EditProfileInfo(request.POST, instance=request.user)
        if profileform.is_valid():
            profileform.save()
            messages.info(request, 'Profile has been updated')
            return redirect('form_app:user_profile')
        else:
            messages(request, 'Invalid details')
    else:
        profileform = EditProfileInfo(instance=request.user)
    context = {
        'profileform': profileform
     }
    return render(request, 'form_app/edit_profile.html', context)


def user_amnt(request, pk):
    amnt = get_object_or_404(UserAmount, pk=pk)
    context = {
        'amnt': amnt
    }
    return render(request, 'form_app/User_amount/user_amount.html', context)


def list_users(request):
    listusers = CustomUser.objects.all()
    count = listusers.count
    context = {
        'listusers': listusers,
        'count': count
    }
    return render(request, 'form_app/Profile/list_users.html', context)


