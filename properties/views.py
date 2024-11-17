from rest_framework import generics, status
from rest_framework.response import Response

from django.db import transaction
from django.core.exceptions import ValidationError

from .models import Property, Address, Photo
from amenities.models import Amenity
from .serializers import PropertySerializer

class PropertiesList(generics.ListCreateAPIView):
    serializer_class = PropertySerializer
    queryset = Property.objects.all()

    # override super class method
    def perform_create(self, serializer):
        address_data = self.request.data.get('address')
        photos_data = self.request.data.get('photos', [])
        amenities_data = self.request.data.get('amenities', [])

        amenities = Amenity.objects.filter(id__in=amenities_data)
        if len(amenities) != len(amenities_data):
            raise ValidationError("Some amenities are not found")

        # insert google maps geocoding below

        with transaction.atomic():

            property_instance = serializer.save()
            property_instance.amenities.set(amenities)

            if address_data:
                Address.objects.create(prop=property_instance, **address_data)
            
            if photos_data:
                for photo in photos_data:
                    Photo.objects.create(prop=property_instance, **photo)