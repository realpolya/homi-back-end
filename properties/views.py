from rest_framework import generics, status
from rest_framework.response import Response

from django.db import transaction
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User
from .models import Property, Address, Photo
from amenities.models import Amenity
from .serializers import PropertySerializer

from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthorized

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


class PropertiesOne(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PropertySerializer
    queryset = Property.objects.all()
    lookup_field = 'id'
    permission_classes = [IsAuthenticated, IsAuthorized]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [] # empty set of permissions
        return super().get_permissions() # default set specified above


class PropertiesUser(generics.ListAPIView):
    serializer_class = PropertySerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Property.objects.none()
        
        return Property.objects.filter(user=user)


class PropertiesMine(generics.ListAPIView):
    serializer_class = PropertySerializer

    def get_queryset(self):
        user = self.request.user
        return Property.objects.filter(user=user)


__all__ = [
    "PropertiesList",
    "PropertiesOne",
    "PropertiesUser",
    "PropertiesMine"
]