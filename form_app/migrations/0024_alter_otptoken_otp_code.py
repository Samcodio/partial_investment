# Generated by Django 5.0.6 on 2024-06-19 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form_app', '0023_alter_otptoken_otp_code_alter_useramount_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='6f4c2f', max_length=6),
        ),
    ]