import logging
logger = logging.getLogger(__name__)

from rest_framework import generics
from datetime import date
from django.utils.timezone import now
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from .models import Booking
from properties.models import Property
from .serializers import BookingSerializer

from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthorized


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
        check_in = date.fromisoformat(self.request.data.get('check_in_date'))
        check_out = date.fromisoformat(self.request.data.get('check_out_date'))
        nights = (check_out - check_in).days

        number_of_guests = self.request.data.get('number_of_guests')
        if number_of_guests > listing.max_guests:
            raise ValidationError("Maximum number of guests is exceeded")

        #TODO: Check if anyone else has already booked the property

        cost = listing.price_per_night * nights
        serializer.save(guest=self.request.user, total_price=cost, prop=listing)


class UpcomingBookings(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(guest=self.request.user, check_in_date__gte=now())


class BookingsOne(generics.RetrieveUpdateDestroyAPIView):
    '''View a single booking by id.
    Only a guest and an associated host can view the booking.
    Only the guest can modify the booking'''
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]
    #TODO: add IsAuthorized for both guest and host

#TODO: create a view for host to view bookings of their properties

__all__ = [
    "BookingsList",
    "BookingsNew",
    "UpcomingBookings",
    "BookingsOne",
]