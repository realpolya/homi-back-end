from django.urls import path
from .views import *

# allows to view all amenities, query amenities, create a new amenity
urlpatterns = [
    path('', PropertiesList.as_view(), name='properties-list')
]