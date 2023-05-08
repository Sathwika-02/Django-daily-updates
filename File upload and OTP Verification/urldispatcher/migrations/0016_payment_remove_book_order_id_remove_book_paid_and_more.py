# Generated by Django 4.2 on 2023-05-01 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('urldispatcher', '0015_book_order_id_book_paid_book_price_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.CharField(max_length=100)),
                ('order_id', models.CharField(blank=True, max_length=100)),
                ('razorpay_payment_id', models.CharField(blank=True, max_length=100)),
                ('paid', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='book',
            name='order_id',
        ),
        migrations.RemoveField(
            model_name='book',
            name='paid',
        ),
        migrations.RemoveField(
            model_name='book',
            name='price',
        ),
        migrations.RemoveField(
            model_name='book',
            name='razorpay_payment_id',
        ),
    ]