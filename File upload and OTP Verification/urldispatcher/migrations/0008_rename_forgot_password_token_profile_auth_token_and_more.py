# Generated by Django 4.2 on 2023-04-20 07:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('urldispatcher', '0007_profile_forgot_password_token'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='forgot_password_token',
            new_name='auth_token',
        ),
        migrations.AddField(
            model_name='profile',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
