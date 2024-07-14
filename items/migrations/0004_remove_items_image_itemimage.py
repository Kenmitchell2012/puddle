# Generated by Django 5.0.6 on 2024-07-11 00:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0003_alter_items_options_alter_items_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='items',
            name='image',
        ),
        migrations.CreateModel(
            name='ItemImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='item_images')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='items.items')),
            ],
        ),
    ]
