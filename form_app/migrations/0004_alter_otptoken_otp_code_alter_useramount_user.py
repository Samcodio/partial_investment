# Generated by Django 5.0.6 on 2024-05-29 23:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form_app', '0003_alter_otptoken_otp_code_alter_useramount_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='774d28', max_length=6),
        ),
        migrations.AlterField(
            model_name='useramount',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='auser', to=settings.AUTH_USER_MODEL),
        ),
    ]