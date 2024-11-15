from django.db import models

# Create your models here.
# creating user model
class User(models.Model):
    name = model.charfield(max_length=40),
    