from rest_framework import generics, status
from rest_framework.response import Response

from django.db import transaction
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User
from .models import Property, Address, Photo
from amenities.models import Amenity
from .serializers import PropertySerializer

from bookings.models import Booking 
from bookings.serializers import BookingSerializer

from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthorized

# google maps
from django.conf import settings
import googlemaps

# available dates filter
from django.utils.dateparse import parse_date


class PropertiesList(generics.ListCreateAPIView):
    '''get list of properties, including filtered / sorted version, create new property, calculate coordinates for address'''
    
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [] # empty set of permissions
        return super().get_permissions() # default set specified above

    def get_queryset(self):

        queryset = Property.objects.filter(is_active=True)

        filter_where = self.request.GET.get('where')
        if filter_where:
            queryset = queryset.filter(address__address_string__icontains=filter_where)
        
        filter_type = self.request.GET.get('type')
        if filter_type:
            queryset = queryset.filter(property_type__iexact=filter_type)
        
        sort_type = self.request.GET.get('sort')
        if sort_type:
            if sort_type == "price":
                queryset = queryset.order_by('price_per_night')
            elif sort_type == "guests":
                queryset = queryset.order_by('max_guests')

        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        if start_date and end_date:
            queryset = self.get_available_props(queryset, start_date, end_date)
        
        return queryset


    def get_available_props(self, queryset, start_date, end_date):
        '''obtain available properties based on the requested dates'''
        avail_start_date = parse_date(start_date)
        avail_end_date = parse_date(end_date)

        if not avail_start_date or not avail_end_date:
            raise ValueError("Invalid dates")
        if avail_start_date >= avail_end_date:
            raise ValueError("Start date can't be later or equal to end date")

        # find all overlapping bookings, extract the ids of the properties
        overlapping_bookings = Booking.objects.filter(
            check_in_date__lte=avail_end_date,
            check_out_date__gte=avail_start_date
        ).values_list('prop_id', flat=True)

        # exclude those properties from the query
        available_props = queryset.exclude(id__in=overlapping_bookings)
        
        return available_props

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
    '''get single property, update and delete the property if authorized'''
    serializer_class = PropertySerializer
    queryset = Property.objects.all()
    lookup_field = 'id'
    permission_classes = [IsAuthenticated, IsAuthorized]


    def get_permissions(self):
        if self.request.method == 'GET':
            return [] # empty set of permissions
        return super().get_permissions() # default set specified above

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
    
    def perform_update(self, serializer):
        try: 

            address_data = self.request.data.get('address')
            photos_data = self.request.data.get('photos', [])
            amenities_data = self.request.data.get('amenities', [])
        
            with transaction.atomic():
                property_instance = serializer.save()

                if amenities_data is not None:

                    amenities = Amenity.objects.filter(id__in=amenities_data)
                    if len(amenities) != len(amenities_data):
                        raise ValidationError("Some amenities are not found")
                    property_instance.amenities.set(amenities)

                if address_data is not None:

                    updated_address, created = Address.objects.update_or_create(
                        prop=property_instance, 
                        defaults=address_data
                    )

                    if not created:
                        for key,value in address_data.items():
                            setattr(updated_address, key, value)
                        updated_address.save()

                    try:
                        coordinates = self.get_coordinates(updated_address.address_string)
                        updated_address.latitude = coordinates[0]
                        updated_address.longitude = coordinates[1]
                    except Exception as e:
                        raise ValidationError(f"Geocoding failed: {str(e)}")
                        
                    updated_address.save()
                
                if photos_data is not None:
                    if not isinstance(photos_data, list):
                        raise ValidationError("Invalid photos data format. Expected a list of URLs.")
                    Photo.objects.filter(prop=property_instance).delete()
                    for photo in photos_data:
                        photo = {key: value for key, value in photo.items() if key != 'prop'}
                        Photo.objects.create(prop=property_instance, **photo)
                
        except Exception as e:

            raise ValidationError({"error": str(e)})


class PropertiesArchived(generics.ListAPIView):
    '''get archived properties corresponding to the logged in user'''
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Property.objects.filter(is_active=False,user=self.request.user)



class PropertiesUser(generics.ListAPIView):
    '''get listed properties corresponding to the requested user'''
    serializer_class = PropertySerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Property.objects.none()
        
        return Property.objects.filter(is_active=True,user=user)



class PropertiesMine(generics.ListAPIView):
    '''get listed properties corresponding to the logged in user'''
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