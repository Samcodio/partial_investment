# Generated by Django 5.0.6 on 2024-06-21 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form_app', '0025_alter_otptoken_otp_code_alter_post_pdf_pdf_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='393b53', max_length=6),
        ),
    ]
