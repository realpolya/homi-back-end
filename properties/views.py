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

# google maps
from django.conf import settings
import googlemaps



class PropertiesList(generics.ListCreateAPIView):
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Property.objects.filter(is_active=True)

        filter_where = self.request.GET.get('where')
        if filter_where:
            queryset = queryset.filter(address__address_string__icontains=filter_where)
        
        return queryset

    def get_permissions(self):
        if self.request.method == 'GET':
            return [] # empty set of permissions
        return super().get_permissions() # default set specified above

    # TODO: filter, sort, search

    def get_coordinates(self, address_string):
        '''obtain latitude and longitude'''
        gmaps = googlemaps.Client(key=settings.GOOGLE_KEY)
        geocode_result = gmaps.geocode(address_string)

        # if address is invalid, return an error
        if not geocode_result:
            raise ValidationError("The address provided is invalid")
        
        # obtaining coordinates from the geocode function
        geo = geocode_result[0].get('geometry')
        geo1 = geo.get('location')
        lat = geo1.get('lat')
        lng = geo1.get('lng')
        coordinates = [lat, lng]
        return coordinates


    # override super class method
    def perform_create(self, serializer):
        address_data = self.request.data.get('address')
        photos_data = self.request.data.get('photos', [])
        amenities_data = self.request.data.get('amenities', [])

        amenities = Amenity.objects.filter(id__in=amenities_data)
        if len(amenities) != len(amenities_data):
            raise ValidationError("Some amenities are not found")
    
        with transaction.atomic():

            property_instance = serializer.save(user=self.request.user)
            property_instance.amenities.set(amenities)

            if address_data:
                new_address = Address.objects.create(prop=property_instance, **address_data)

                try:
                    coordinates = self.get_coordinates(new_address.address_string)
                    new_address.latitude = coordinates[0]
                    new_address.longitude = coordinates[1]
                except Exception as e:
                    raise ValidationError(f"Geocoding failed: {str(e)}")
                    
                new_address.save()
            
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


class PropertiesArchived(generics.ListAPIView):
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Property.objects.filter(is_active=False,user=self.request.user)



class PropertiesUser(generics.ListAPIView):
    serializer_class = PropertySerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Property.objects.none()
        
        return Property.objects.filter(is_active=True,user=user)



class PropertiesMine(generics.ListAPIView):
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Property.objects.filter(is_active=True,user=user)


__all__ = [
    "PropertiesList",
    "PropertiesOne",
    "PropertiesArchived",
    "PropertiesUser",
    "PropertiesMine",
]