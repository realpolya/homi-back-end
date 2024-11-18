from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User

from amenities.models import Amenity

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
    amenities = models.ManyToManyField(Amenity)
    is_active = models.BooleanField(default=True)
    cleaning_fee = models.IntegerField(default=0)
    cancellation_policy = models.CharField(
        max_length=20,
        choices=CANCELLATION,
        default=CANCELLATION[0] 
    )
    
    def __str__(self):
        return self.title


class Photo(models.Model):
    prop = models.ForeignKey(
        Property, 
        on_delete=models.CASCADE, 
        related_name='photos'
    )
    link = models.URLField(max_length=300)


class Address(models.Model):
    prop = models.OneToOneField(
        Property, 
        on_delete=models.CASCADE,
        related_name='address'
    )
    street = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    state = models.CharField(
        max_length=250,
        choices=STATES,
        default=STATES[0] 
    )
    zip_code = models.CharField(max_length=6)
    country = models.CharField(max_length=20, default="USA")
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)

    @property
    def address_string(self):
        return f"{self.street}, {self.city}, {self.state}, {self.country}"


