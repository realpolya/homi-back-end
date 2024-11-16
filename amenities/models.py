from django.db import models

# Create your models here.
class Amenity(models.Model):
    name = models.CharField(max_length=100)
    image = models.URLField(max_length=300)

    def __str__(self):
        return self.name