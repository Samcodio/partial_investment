# Generated by Django 5.0.6 on 2024-05-29 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form_app', '0004_alter_otptoken_otp_code_alter_useramount_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='2f0708', max_length=6),
        ),
    ]
