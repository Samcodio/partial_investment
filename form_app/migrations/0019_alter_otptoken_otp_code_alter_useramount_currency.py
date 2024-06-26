# Generated by Django 5.0.6 on 2024-06-16 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form_app', '0018_alter_otptoken_otp_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='588653', max_length=6),
        ),
        migrations.AlterField(
            model_name='useramount',
            name='currency',
            field=models.CharField(blank=True, choices=[('£', '£'), ('$', '$'), ('₱', '₱'), ('S$', 'S$'), ('฿', '฿'), ('د.إ', 'د.إ'), ('R', 'R'), ('AU$', 'AU$')], default='$', max_length=30, null=True),
        ),
    ]
