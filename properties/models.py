from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.


class Property(models.Model):

    PROPERTY_TYPE = (
        ('Entire Place', 'Entire Place'),
        ('Private Room', 'Private Room'),
        ('Shared Room', 'Shared Room'),
        ('Vacation Home', 'Vacation Home'),
        ('Loft', 'Loft'),
        ('Hostel', 'Hostel'),
        ('Mansion', 'Mansion'),
        ('Villa', 'Villa'),
        ('Castle', 'Castle'),
        ('Luxury Apartment', 'Luxury Apartment')
    )


    CANCELLATION = (
    ("Flexible", "Receive a full refund if canceled at least 24 hours before check-in; after that, no refund."),
    ("Moderate", "Receive a full refund if canceled at least 5 days before check-in; first night non-refundable after that."),
    ("Strict", "Receive half a refund if canceled at least 14 days before check-in; no refund after that."),
    ("Long-Term", "Receive a full refund if canceled at least 30 days before check-in; no refund after that."),
    ("Super Strict 30 Days", "You will receive half a refund if canceled at least 30 days before check-in; no refund after that."),
    ("Super Strict 60 Days", "You will receive half a refund if canceled at least 60 days before check-in; no refund after that."),
    ("Non-Refundable", "No refund if canceled at any time.")
    )

    #Amenities = Amenities_list



    title = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    price_per_night = models.IntegerField()
    max_guests = models.IntegerField()
    property_type = models.CharField(
        max_length=20,
        choices=PROPERTY_TYPE,
        default=PROPERTY_TYPE[0][0] 
    )
    

    amenities = ArrayField(
            models.CharField(max_length=50, choices=AMENITIES), ##This needs to be fixed once i get Polina's Amenities list
            blank=True
    
    )
    is_active = models.BooleanField()
    cleaning_fee = models.IntegerField()
    cancellation_policy = models.CharField(
        max_length=20,
        coices=CANCELLATION
    )

    photos = ArrayField(
        models.URLField(max_length=200),
        blank=True
    )

    def __str__(self):
        return self.title

    


