import secrets
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from django.core.mail import send_mail
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse

# Create your models here.


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    account_number = models.IntegerField(max_length=10, null=True, blank=True, editable=True)
    account_name = models.CharField(max_length=40, null=True, blank=True, editable=True)

    USERNAME_FIELD = ("email")
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email


class Otptoken(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='otps')
    otp_code = models.CharField(max_length=6, default=secrets.token_hex(3))
    otp_created_at = models.DateTimeField(auto_now_add=True)
    otp_expires_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.user.username


class Post_pdf(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    pdf_name = models.CharField(max_length=50)
    pdf_file = models.FileField(upload_to='pdfs/')
    posted_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.pdf_name

    class Meta:
        ordering = ['posted_on']

    def get_absolute_url(self):
        return reverse('form_app:pdf_details', args=[self.id])


@receiver(post_save, sender=CustomUser)
def create_token(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser:
            pass
        else:
            Otptoken.objects.create(user=instance, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))
            instance.is_active = False
            instance.save()

        # email credentials
        otp = Otptoken.objects.filter(user=instance).last()
        subject = "Email Verification"
        message = f"""
                        Hello, {instance.username}
                        Your OTP is {otp.otp_code}
                        It expires in 5 minutes. Use the link to return to the webpage\n
                        http://1270.0.0.1.8000/verify-email/{instance.username}
                """
        sender = "nosikesamuel1@gmail.com"
        receiver = [instance.email, ]



        #send email
        send_mail(
            subject,
            message,
            sender,
            receiver,
            fail_silently=False
        )
