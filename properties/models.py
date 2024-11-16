from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User

from .amenities import AMENITIES
from .states import STATES
from .property_type import PROPERTY_TYPE
from .cancellation import CANCELLATION


class Property(models.Model):
    title = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=500)
    price_per_night = models.IntegerField()
    max_guests = models.IntegerField()
    property_type = models.CharField(
        max_length=20,
        choices=PROPERTY_TYPE,
        default=PROPERTY_TYPE[0] 
    )
    amenities = ArrayField(
            models.CharField(max_length=90, choices=AMENITIES), 
            blank=True
    )
    is_active = models.BooleanField(default=True)
    cleaning_fee = models.IntegerField(default=0)
    cancellation_policy = models.CharField(
        max_length=20,
        choices=CANCELLATION
    )
    photos = ArrayField(
        models.URLField(max_length=200),
        blank=True
    )

    def __str__(self):
        return self.title


class Address(models.Model):
    prop = models.OneToOneField(Property, on_delete=models.CASCADE)
    street = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    state = models.CharField(
        max_length=250,
        choices=STATES,
        default=STATES[0] 
    )
    zip_code = models.CharField(max_length=6)
    country = models.CharField(max_length=20, default="United States")
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)


