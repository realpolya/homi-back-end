import logging
logger = logging.getLogger(__name__)

from rest_framework import generics
from datetime import date
from django.utils.timezone import now
from django.utils.dateparse import parse_date
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from .models import Booking
from properties.models import Property
from users.models import Profile
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


    def get_availability(self, listing, check_in, check_out):
        '''obtain availability of the requested property'''

        if not check_in or not check_out:
            raise ValueError("Invalid dates")
        if check_in >= check_out:
            raise ValueError("Check in date can't be later or equal to check out date")

        overlapping_bookings = Booking.objects.filter(
            prop_id=listing.id,
            check_in_date__lte=check_out,
            check_out_date__gte=check_in
        )

        if len(overlapping_bookings) != 0:
            return False
        
        return True


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

        availability_check = self.get_availability(listing, check_in, check_out)
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


class BookingsOne(generics.RetrieveUpdateDestroyAPIView):
    '''View a single booking by id.
    Only a guest and an associated host can view the booking.
    Only the guest can modify the booking'''
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]
    #TODO: add IsAuthorized for both guest and host

    #TODO: subtract from host's profits if booking is deleted

#TODO: create a view for host to view bookings of their properties

__all__ = [
    "BookingsList",
    "BookingsNew",
    "UpcomingBookings",
    "BookingsOne",
]