# from django.shortcuts import render


from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
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
