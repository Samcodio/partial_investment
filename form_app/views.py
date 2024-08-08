from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
import boto3
from django.conf import settings
from datetime import datetime, timedelta
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site

# Create your views here.


# def TopUpAccount(request):
#     return render(request, 'Users/TopUpAccount.html')


def home(request):
    context = {}
    return render(request, 'Users/dashboard.html', context)

@login_required()
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
    return render(request, 'PdfList/List.html', context)

@login_required()
def setting(request):
    context = {}
    return render(request, 'form_app/settings.html', context)

# @login_required()
# def post_pdf(request):
#     form = post_form()
#     if request.method == 'POST':
#         form = post_form(request.POST, request.FILES)
#         if form.is_valid():
#             instance = form.save(commit=False)
#             instance.user = request.user
#             instance.save()
#             return redirect('form_app:list_pdf')
#         else:
#             messages.error(request, 'Invalid details')
#     context = {
#         'form': form
#     }
#     return render(request, 'form_app/Posts/create_post.html', context)


@login_required
def post_pdf(request):
    form = post_form()
    if request.method == 'POST':
        form = post_form(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = request.FILES.get('pdf_file')

            if pdf_file:
                s3_client = boto3.client(
                    's3',
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    region_name=settings.AWS_S3_REGION_NAME,
                )

                # Define the file path in S3 bucket
                file_path = f'pdfs/{pdf_file.name}'
                expiration_date = datetime.now() + timedelta(days=90)

                try:
                    s3_client.upload_fileobj(
                        pdf_file,
                        settings.AWS_STORAGE_BUCKET_NAME,
                        file_path,
                        ExtraArgs = {'ACL': 'public-read',
                                     'Metadata': {
                                         'expiration_date': expiration_date.strftime('%Y-%m-%d')
                                     }
                                 }
                    )

                    pdf_url = s3_client.generate_presigned_url(
                        'get_object',
                        Params={
                            'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                            'Key': file_path
                        },
                        ExpiresIn=86400
                    )

                    # If upload is successful, save the URL to the model instance
                    instance = form.save(commit=False)
                    instance.user = request.user
                    instance.pdf_url = pdf_url
                    instance.save()

                    return redirect('form_app:list_pdf')
                except Exception as e:
                    messages.error(request, f'Error uploading file: {str(e)}')
            else:
                messages.error(request, 'No PDF file provided')
        else:
            messages.error(request, 'Invalid details')

    context = {
        'form': form
    }
    return render(request, 'form_app/Posts/create_post.html', context)


def pdf_details(request, pk):
    pdfdetails = get_object_or_404(Post_pdf, pk=pk)
    # pdf_page = pdfdetails.pdf_file
    # response = HttpResponse(pdf_page.read(), content_type='application/pdf')
    # return response
    if request.method == 'POST':
        pdfdetails.delete()
        return redirect('form_app:list_pdf')
    context = {
        'pdfdetails': pdfdetails
    }
    return render(request, 'form_app/Posts/details.html', context)


def display_pdf(request, pk):
    pdf_content = get_object_or_404(Post_pdf, pk=pk)
    context = {
        'pdf_content': pdf_content
    }
    return render(request, 'form_app/Posts/display_pdf.html', context)


def verify_email(request, username):
    user = CustomUser.objects.get(username=username)
    user_otp = Otptoken.objects.filter(user=user).last()
    if request.method == 'POST':
        if user_otp.otp_code == request.POST['otp_code']:

            # not expired
            if user_otp.otp_expires_at > timezone.now():
                user.is_active = True
                user.save()
                messages.success(request, "Account successfully created")
                return redirect("user_login:login")
            # expired
            else:
                messages.warning(request, "This OTP has expired, please get a new OTP")
                return redirect('form_app:verify_email', username=user.username)

        # invalid otp
        else:
            messages.warning(request, "Invalid OTP entered")
            return redirect('form_app:verify_email', username=user.username)
    context = {}
    return render(request, 'Authentications/otpVerify.html', context)


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
                                    It expires in 5 minutes.\n
                                    https://foundever.info/verify-email/{user.username}/
                                    
                            """
            sender = "foundeveruk@gmail.com"
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

@login_required()
def profile_page(request):
    userdetails = request.user

    if request.method == 'POST':
        messages.success(request, 'Withdrawal Pending')
        #             email variables
        subject = "Email Verification"
        message = f"""
                                            Hello Sir, {request.user.username}
                                            is trying to withdraw his balance
                                            I suggest you take action soon
                                    """
        sender = "foundeveruk@gmail.com"
        receiver = ["foundeveruk@gmail.com"]

        # send email
        send_mail(
            subject,
            message,
            sender,
            receiver,
            fail_silently=False
        )
    context = {
        'userdetails': userdetails
    }
    return render(request, 'Users/profile.html', context)


@login_required()
def edit_profile(request):
    profileform = EditProfileInfo(instance=request.user)
    if request.method == 'POST':
        profileform = EditProfileInfo(request.POST, instance=request.user)
        if profileform.is_valid():
            profileform.save()
            return redirect('form_app:user_profile')
        else:
            messages(request, 'Invalid details')
    else:
        profileform = EditProfileInfo(instance=request.user)
    context = {
        'profileform': profileform
     }
    return render(request, 'Users/setting.html', context)

@login_required()
def user_amnt(request, pk):
    amnt = get_object_or_404(UserAmount, pk=pk)
    context = {
        'amnt': amnt
    }
    return render(request, 'form_app/User_amount/user_amount.html', context)

@login_required()
def list_users(request):
    listusers = CustomUser.objects.all().order_by('email')[:150]
    count = listusers.count
    context = {
        'listusers': listusers,
        'count': count
    }
    return render(request, 'Admin/userList.html', context)

@login_required()
def userlist(request):
    listusers = CustomUser.objects.all().order_by('email')[150:300]
    count = listusers.count
    context = {
        'listusers': listusers,
        'count': count
    }
    return render(request, 'Admin/List.html', context)


@login_required()
def userlist3(request):
    listusers = CustomUser.objects.all().order_by('email')[300:450]
    count = listusers.count
    context = {
        'listusers': listusers,
        'count': count
    }
    return render(request, 'Admin/userList3.html', context)


@login_required()
def adjust_amount(request, pk):
    current_amount = get_object_or_404(UserAmount, pk=pk)
    updforum = AdjustAmount(instance=current_amount)
    if request.method == 'POST':
        updforum = AdjustAmount(request.POST, instance=current_amount)
        if updforum.is_valid():
            updforum.save()
            return redirect('form_app:list_users')
    else:
        pass
        updforum = AdjustAmount(instance=current_amount)
    context = {
        'updforum': updforum,
    }
    return render(request, 'Users/TopUpAccount.html', context)


def T_and_C(request):
    context = {}
    return render(request, 'Authentications/TandC.html', context)


@permission_required('is_superuser')
def deactivation(request, id):
    user = CustomUser.objects.get(id=id)
    if request.method == 'POST':
        if user.is_superuser:
            return redirect('form_app:home')
        else:
            user.is_active = False
            user.save()
            return redirect('form_app:list_users')
            messages.success(request, f'{user.username} is deactivated')
    context = {
        'user': user
    }
    return render(request, 'Admin/deactivate.html', context)


@permission_required('is_superuser')
def reactivation(request, id):
    user = CustomUser.objects.get(id=id)
    if request.method == 'POST':
        user.is_active = True
        user.save()
        return redirect('form_app:list_users')
        messages.success(request, f'{user.username} is reactivated')
    context = {
        'user': user
    }
    return render(request, 'Admin/reactivate.html', context)


@permission_required('is_superuser')
def deletion(request, id):
    user = CustomUser.objects.get(id=id)
    if request.method == 'POST':
        if user.is_superuser:
            return redirect('form_app:home')
        else:
            user.delete()
            return redirect('form_app:list_users')
    context = {
        'user': user
    }
    return render(request, 'Admin/deletion.html', context)


def forgot_password_email(request):
    if request.method == 'POST':
        user_email = request.POST["last_email"]

        if CustomUser.objects.filter(email=user_email).exists():
            user = CustomUser.objects.get(email=user_email)

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            domain = 'foundever.info'
            protocol = 'https' if request.is_secure() else 'http'

            subject = "Password Reset Requested"
            message = render_to_string('registration/password_reset_email.html', {
                'domain': domain,
                'protocol': protocol,
                'uid': uid,
                'token': token,
                'user': user,
                'site_name': current_site.name,
            })

            sender = "foundeveruk@gmail.com"
            receiver = [user.email, ]

            # send email
            send_mail(
                subject,
                message,
                sender,
                receiver,
                fail_silently=False

            )
            return redirect('form_app:password_reset_done')
        else:
            messages.warning(request, 'PLease enter the email used')
            return redirect('form_app:forgot_password_email')
    context = {}
    return render(request, 'form_app/Verification/forgot.html', context)


def PasswordResetDoneView(request):
    context = {}
    return render(request, 'form_app/Password_reset/password_reset_done.html')




