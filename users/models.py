from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    googleId = models.CharField(default="")
    profile_pic = models.CharField(default="")
    bio = models.CharField(default="")
    is_host = models.BooleanField(default=False)
    profits = models.FloatField(default=0)
    
    def __str__(self):
        return f"{self.user.username}'s profile"