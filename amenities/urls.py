from django.urls import path
from .views import *

# allows to view all amenities, query amenities, create a new amenity
urlpatterns = [
    path('', AmenitiesList.as_view(), name='amenities-list')
]