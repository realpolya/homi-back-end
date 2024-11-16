# Generated by Django 5.1.3 on 2024-11-16 15:05

import django.contrib.postgres.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=500)),
                ('price_per_night', models.IntegerField()),
                ('max_guests', models.IntegerField()),
                ('property_type', models.CharField(choices=[('EN', 'Entire Place'), ('PR', 'Private Room'), ('SH', 'Shared Room'), ('VA', 'Vacation Home'), ('LO', 'Loft'), ('HO', 'Hostel'), ('MA', 'Mansion'), ('VI', 'Villa'), ('CA', 'Castle'), ('LU', 'Luxury Apartment')], default=('EN', 'Entire Place'), max_length=20)),
                ('amenities', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('Heating', 'https://www.reshot.com/preview-assets/icons/VJLXFPZWAB/water-heating-VJLXFPZWAB.svg'), ('Air Conditioning', 'https://www.reshot.com/preview-assets/icons/5MUHFP6QBZ/air-conditioning-5MUHFP6QBZ.svg'), ('WiFi', 'https://www.reshot.com/preview-assets/icons/DQZC9PBJME/wifi-DQZC9PBJME.svg'), ('Parking', 'https://www.reshot.com/preview-assets/icons/YW4CGQ8JEV/parking-YW4CGQ8JEV.svg'), ('Gym', 'https://www.reshot.com/preview-assets/icons/WS79HTVFXE/gym-dumbbell-WS79HTVFXE.svg'), ('Pool', 'https://www.reshot.com/preview-assets/icons/RMA9GY5SEX/swimming-pool-RMA9GY5SEX.svg'), ('Hot Tub', 'https://www.reshot.com/preview-assets/icons/5EPTZWL79S/hot-tub-5EPTZWL79S.svg'), ('Kitchen', 'https://www.reshot.com/preview-assets/icons/YF9WTCLDKV/kitchen-sink-YF9WTCLDKV.svg'), ('Dishes and Silverware', 'https://www.reshot.com/preview-assets/icons/TBDKN36ULZ/dishes-TBDKN36ULZ.svg'), ('Dishwasher', 'https://www.reshot.com/preview-assets/icons/Q3YBKWC2TU/clean-dishes-Q3YBKWC2TU.svg'), ('TV', 'https://www.reshot.com/preview-assets/icons/ZRPASWEJTX/tv-ZRPASWEJTX.svg'), ('Board Games', 'https://www.reshot.com/preview-assets/icons/3SRUDQLYH5/board-game-3SRUDQLYH5.svg'), ('Patio', 'https://www.reshot.com/preview-assets/icons/7WMD2JRUPE/deck-chair-7WMD2JRUPE.svg'), ('Backyard', 'https://www.reshot.com/preview-assets/icons/LK3RW8HNJZ/tree-LK3RW8HNJZ.svg'), ('Washer and Dryer', 'https://www.reshot.com/preview-assets/icons/5E6SCBK2HW/washer-machine-5E6SCBK2HW.svg'), ('Iron', 'https://www.reshot.com/preview-assets/icons/V8S5HG9YE2/ironing-clothes-V8S5HG9YE2.svg'), ('Hair Dryer', 'https://www.reshot.com/preview-assets/icons/FBW8GZ26NS/hair-dryer-FBW8GZ26NS.svg'), ('Shampoo', 'https://www.reshot.com/preview-assets/icons/D9EJMRAVTS/shampoo-D9EJMRAVTS.svg'), ('Conditioner', 'https://www.reshot.com/preview-assets/icons/8M96ST4VA5/shampoo-8M96ST4VA5.svg'), ('Bathtub', 'https://www.reshot.com/preview-assets/icons/SWRXC3L48F/clean-bathtub-SWRXC3L48F.svg'), ('Smoke Alarm', 'https://www.reshot.com/preview-assets/icons/YJETM7HGRF/smoke-detector-YJETM7HGRF.svg'), ('Self check-in', 'https://www.reshot.com/preview-assets/icons/28QDAR4CPV/check-in-28QDAR4CPV.svg')], max_length=50), blank=True, size=None)),
                ('is_active', models.BooleanField(default=True)),
                ('cleaning_fee', models.IntegerField(default=0)),
                ('cancellation_policy', models.CharField(choices=[('Flexible', 'Receive a full refund if canceled at least 24 hours before check-in; after that, no refund.'), ('Moderate', 'Receive a full refund if canceled at least 5 days before check-in; first night non-refundable after that.'), ('Strict', 'Receive half a refund if canceled at least 14 days before check-in; no refund after that.'), ('Long-Term', 'Receive a full refund if canceled at least 30 days before check-in; no refund after that.'), ('Super Strict 30 Days', 'You will receive half a refund if canceled at least 30 days before check-in; no refund after that.'), ('Super Strict 60 Days', 'You will receive half a refund if canceled at least 60 days before check-in; no refund after that.'), ('Non-Refundable', 'No refund if canceled at any time.')], max_length=20)),
                ('photos', django.contrib.postgres.fields.ArrayField(base_field=models.URLField(), blank=True, size=None)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=250)),
                ('city', models.CharField(max_length=250)),
                ('state', models.CharField(choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], default=('AL', 'Alabama'), max_length=250)),
                ('zip_code', models.CharField(max_length=6)),
                ('country', models.CharField(default='United States', max_length=20)),
                ('latitude', models.FloatField(default=0.0)),
                ('longitude', models.FloatField(default=0.0)),
                ('prop', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='properties.property')),
            ],
        ),
    ]
