from rest_framework import generics, status
from rest_framework.response import Response

from datetime import date
from django.utils.timezone import now
from django.utils.dateparse import parse_date
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from .models import Booking
from properties.models import Property
from users.models import Profile
from .serializers import BookingSerializer

from .utils import get_availability

from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthorizedGuestHost, IsAuthorizedGuest, IsAuthorizedHost


class BookingsList(generics.ListAPIView):
    '''Guest's bookings. Only a guest can view their bookings.'''
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Booking.objects.filter(guest=self.request.user)
        return queryset


class BookingsNew(generics.CreateAPIView):
    '''User creates new booking'''
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer):

        # find associated property
        prop_id = self.kwargs.get('prop_id')
        try:
            listing = Property.objects.get(id=prop_id)
        except ObjectDoesNotExist:
            raise ValidationError("Property with this ID does not exist")
        
        # calculate total based on property's price
        check_in = parse_date(self.request.data.get('check_in_date'))
        check_out = parse_date(self.request.data.get('check_out_date'))
        nights = (check_out - check_in).days

        number_of_guests = self.request.data.get('number_of_guests')
        if number_of_guests > listing.max_guests:
            raise ValidationError("Maximum number of guests is exceeded")

        availability_check = get_availability(listing, check_in, check_out)
        if not availability_check:
            raise ValidationError("This property is already booked for the requested dates")

        nights_cost = listing.price_per_night * nights

        # update host's profits
        host_profile = Profile.objects.get(user=listing.user)
        host_profile.profits += nights_cost
        host_profile.save()

        cost = nights_cost + listing.cleaning_fee
        serializer.save(guest=self.request.user, total_price=cost, prop=listing)


class UpcomingBookings(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(guest=self.request.user, check_in_date__gte=now())


class PreviousBookings(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(guest=self.request.user, check_out_date__lte=now())


class BookingsOne(generics.RetrieveUpdateDestroyAPIView):
    '''View a single booking by id.
    Only a guest and an associated host can view the booking.
    Only the guest can modify the booking'''
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated, IsAuthorizedGuestHost]


    def get_permissions(self):
        # only guest can change or delete their booking
        if self.request.method != 'GET':
            return [IsAuthenticated(), IsAuthorizedGuest()]
        # only guest and host can view the booking
        return super().get_permissions()
    

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=kwargs.get('partial', False))

        try:
            listing = Property.objects.get(id=instance.prop_id)
        except ObjectDoesNotExist:
            raise ValidationError("Property with this ID does not exist")

        # only has logic for when BOTH check in and check out dates are provided
        if 'check_in_date' in request.data and 'check_out_date' in request.data:

            check_in = parse_date(self.request.data.get('check_in_date'))
            check_out = parse_date(self.request.data.get('check_out_date'))

            if check_in and check_out:

                availability_check = get_availability(listing, check_in, check_out, instance)
                if not availability_check:
                    raise ValidationError("This property is already booked for the requested dates")

                nights = (check_out - check_in).days
                nights_cost = listing.price_per_night * nights
            else:
                raise ValidationError("Dates provided were not parsed properly")

            # update host's profits
            host_profile = Profile.objects.get(user=listing.user)
            host_profile.profits -= instance.total_price
            host_profile.profits += nights_cost
            host_profile.save()

            cost = nights_cost + listing.cleaning_fee

            instance.check_in_date = check_in
            instance.check_out_date = check_out
            instance.total_price = cost


        if 'number_of_guests' in request.data:

            number_of_guests = self.request.data.get('number_of_guests')
            if number_of_guests > listing.max_guests:
                raise ValidationError("Maximum number of guests is exceeded")
            
            instance.number_of_guests = number_of_guests
        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)
    

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()

        try:
            listing = Property.objects.get(id=instance.prop_id)
        except ObjectDoesNotExist:
            raise ValidationError("Property with this ID does not exist")
        
        host_profile = Profile.objects.get(user=listing.user)
        host_profile.profits -= instance.total_price
        host_profile.profits += listing.cleaning_fee
        host_profile.save()

        self.perform_destroy(instance)
        return Response({"message": "Object deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class BookingsHost(generics.ListAPIView):
    '''Bookings of host's properties.'''
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Booking.objects.filter(prop__user=self.request.user)
        return queryset



class BookingsProperty(generics.ListAPIView):
    '''Bookings of a particular property.'''
    serializer_class = BookingSerializer
    # permission_classes = [IsAuthenticated, IsAuthorizedHost]

    def get_queryset(self):
        prop_id = self.kwargs.get('prop_id')
        queryset = Booking.objects.filter(prop_id=prop_id)
        return queryset



__all__ = [
    "BookingsList",
    "BookingsNew",
    "UpcomingBookings",
    "PreviousBookings",
    "BookingsOne",
    "BookingsHost",
    "BookingsProperty"
]