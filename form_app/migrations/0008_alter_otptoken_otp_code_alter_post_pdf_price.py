# Generated by Django 5.0.6 on 2024-06-07 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form_app', '0007_alter_otptoken_otp_code_alter_post_pdf_posted_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='da4614', max_length=6),
        ),
        migrations.AlterField(
            model_name='post_pdf',
            name='price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]