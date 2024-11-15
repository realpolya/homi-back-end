from django.db import models


# Create your models here.
class Booking (models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    total_price = models.IntegerField()
    message = models.TextField()
    number_of_guests = models.IntegerField()
    credit_card = models.IntegerField(default=0000000000000000)
    
