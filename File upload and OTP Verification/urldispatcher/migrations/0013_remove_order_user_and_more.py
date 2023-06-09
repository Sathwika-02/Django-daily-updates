# Generated by Django 4.2 on 2023-04-28 06:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('urldispatcher', '0012_cart_product_order_productioncart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='user',
        ),
        migrations.AlterUniqueTogether(
            name='productioncart',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='productioncart',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='productioncart',
            name='product',
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.DeleteModel(
            name='ProductionCart',
        ),
    ]
