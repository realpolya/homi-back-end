# from django.shortcuts import render


from rest_framework import generics, permissions
from django.utils.timezone import now
from .models import Booking
from .serializers import BookingSerializer


class CreateBookingAPIView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    #only those that are authenticated can create a booking
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self,serializer):
        serializer.save(guest=self.request.user)


class BookingAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    #only those that are authenticated can also view and update their booking
    permission_classes = [permissions.IsAuthenticated]


class UpcomingBookingsAPIView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(guest=self.request.user, check_in_date__gte=now())
