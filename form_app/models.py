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
    Status_choices = [
        ('Select Your Bank', 'Select Your Bank'),
        ('SEA Bank', 'SEA Bank'),
        ('BPI Bank', 'BPI Bank'),
        ('KOMO Bank', 'KOMO Bank'),
        ('Gcash account', 'Gcash account'),
        ('U.S. Bank', 'U.S. Bank'),
        ('Citi Bank', 'Citi Bank'),
        ('PNC Financial Services Group, Inc', 'PNC Financial Services Group, Inc'),
        ('DBS Group Holdings Ltd', 'DBS Group Holdings Ltd'),
        ('Oversea-Chinese Banking Corporation', 'Oversea-Chinese Banking Corporation'),
        ('United Overseas Bank Ltd', 'United Overseas Bank Ltd'),
        ('Hongkong Shanghai Banking Corporation Limited', 'Hongkong Shanghai Banking Corporation Limited'),
        ('Royal Bank of Canada', 'Royal Bank of Canada'),
        ('Toronto-Dominion Bank', 'Toronto-Dominion Bank'),
        ('Bank of Nova Scotia', 'Bank of Nova Scotia'),
        ('Bank of Montreal', 'Bank of Montreal'),
        ('Canadian Imperial Bank of Commerce', 'Canadian Imperial Bank of Commerce'),
        ('Bangkok Bank', 'Bangkok Bank'),
        ('Tisco Bank', 'Tisco Bank'),
        ('SCB account', 'SCB account'),
        ('Lloyds Bank', 'Lloyds Bank'),
        ('Royal Bank', 'Royal Bank'),
        ('Barclays account', 'Barclays account'),
        ('Emirates NBD Bank', 'Emirates NBD Bank'),
        ('Dubai Islamic Bank', 'Dubai Islamic Bank'),
        ('Mashreq Bank', 'Mashreq Bank'),
        ('Union National Bank', 'Union National Bank'),
        ('Standard Bank', 'Standard Bank'),
        ('FirstRand Limited', 'FirstRand Limited'),
        ('Absa group', 'Absa group'),
        ('Nedbank', 'Nedbank'),
        ('Investec Bank', 'Investec bank'),
        ('KB Kookim Bank', 'KB Kookim Bank'),
        ('Shinhan Bank', 'Shinhan Bank'),
        ('Nonghyup Bank', 'Nonghyup Bank'),
        ('Hana Financial Group', 'Hana Financial Group'),
    ]
    email = models.EmailField(unique=True)
    bank_name = models.CharField(max_length=50, choices=Status_choices)
    account_number = models.CharField(max_length=10, null=True, blank=True)
    account_name = models.CharField(max_length=40, null=True, blank=True)

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
    price = models.IntegerField(null=True, blank=True)
    posted_on = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.pdf_name

    class Meta:
        ordering = ['posted_on']

    def get_absolute_url(self):
        return reverse('form_app:pdf_details', args=[self.id])


class UserAmount(models.Model):
    STATUS_CHOICES = [('\u00A3', '\u00A3'),
                      ('\u0024', '\u0024'),
                      ('\u20B1', '\u20B1'),
                      ('S\u0024', 'S\u0024'),
                      ('\u0E3F', '\u0E3F'),
                      ('\u062F\u002E\u0625', '\u062F\u002E\u0625'),
                      ('R', 'R'),
                      ('AU\u0024', 'AU\u0024'),
                      ]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='auser')
    currency = models.CharField(max_length=30, default='\u0024', null=True, blank=True, choices=STATUS_CHOICES)
    amount = models.IntegerField(null=True, blank=True)

    def __int__(self):
        return self.amount

    def get_absolute_url(self):
        return reverse('form_app:user_amount', args=[self.pk])


@receiver(post_save, sender=CustomUser)
def create_token(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser:
            UserAmount.objects.create(user=instance, amount=0)
            Otptoken.objects.create(user=instance, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))
            pass
        else:
            UserAmount.objects.create(user=instance, amount=0)
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
                        https://foundever.uk/verify-email/{instance.username}/
                        
                """
        sender = "foundeveruk@gmail.com"
        receiver = [instance.email, ]



        #send email
        send_mail(
            subject,
            message,
            sender,
            receiver,
            fail_silently=False
        )
