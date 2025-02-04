# Generated by Django 5.0.6 on 2024-10-31 00:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='address',
            new_name='shipping_address',
        ),
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='city',
            new_name='shipping_city',
        ),
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='country',
            new_name='shipping_country',
        ),
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='email',
            new_name='shipping_email',
        ),
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='fullname',
            new_name='shipping_fullname',
        ),
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='phone_number',
            new_name='shipping_phone_number',
        ),
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='state',
            new_name='shipping_state',
        ),
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='zip_code',
            new_name='shipping_zip_code',
        ),
    ]
