from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from properties.models import Property
from datetime import date

# Create your models here.
class Booking (models.Model):
    prop = models.ForeignKey(Property, on_delete=models.CASCADE)
    guest = models.ForeignKey(User, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    total_price = models.IntegerField(default=0)
    message = models.TextField()
    number_of_guests = models.IntegerField(default=1)
    credit_card = models.IntegerField(default=0000000000000000)

    def clean(self):
        today = date.today()

        if self.check_in_date <= today:
            raise ValidationError("Check-in date must be later than today.")
        if self.check_out_date <= today:
            raise ValidationError("Check-out date must be later than today.")
        if self.check_in_date >= self.check_out_date:
            raise ValidationError("Check-out date must be later than check-in date.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


    def __str__(self):
        return f'{self.prop.title} booked from {self.check_in_date} to {self.check_out_date}'