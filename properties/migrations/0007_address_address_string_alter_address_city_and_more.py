# Generated by Django 5.1.3 on 2024-11-18 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0006_alter_address_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='address_string',
            field=models.CharField(default='TEMPORARY', max_length=250),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='address',
            name='street',
            field=models.CharField(max_length=100),
        ),
    ]