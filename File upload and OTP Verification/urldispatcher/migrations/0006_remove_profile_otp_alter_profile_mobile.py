# Generated by Django 4.2 on 2023-04-18 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('urldispatcher', '0005_remove_profile_auth_token_remove_profile_created_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='otp',
        ),
        migrations.AlterField(
            model_name='profile',
            name='mobile',
            field=models.CharField(max_length=10),
        ),
    ]