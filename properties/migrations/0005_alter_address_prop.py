# Generated by Django 5.1.3 on 2024-11-17 17:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0004_remove_property_amenities_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='prop',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='address', to='properties.property'),
        ),
    ]
