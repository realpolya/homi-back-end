from django.db import models
from .amenities import AMENITIES
from .property_type import PROPERTY_TYPE
from .cancellation import CANCELLATION
from django.contrib.postgres.fields import ArrayField


# Create your models here.


class Property(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    price_per_night = models.IntegerField()
    max_guests = models.IntegerField()
    property_type = models.CharField(
        max_length=20,
        choices=PROPERTY_TYPE,
        default=PROPERTY_TYPE[0] 
    )
    

    amenities = ArrayField(
            models.CharField(max_length=50, choices=AMENITIES), 
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

    


