from django.urls import path
from .views import CreateBookingAPIView, BookingAPIView, UpcomingBookingsAPIView

urlpatterns = [
    
    path('bookings/', CreateBookingAPIView.as_view(), name='create-booking'),
    

    path('bookings/<int:pk>/', BookingAPIView.as_view(), name='manage-booking'),
    
    
    path('bookings/upcoming/', UpcomingBookingsAPIView.as_view(), name='upcoming-bookings'),
]
