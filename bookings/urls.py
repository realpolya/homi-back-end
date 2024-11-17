from django.urls import path
from . import views

urlpatterns = [

    path('bookings/', views.UpcomingBookingsAPIView.as_view(), name='upcoming-bookings'),


    path('bookings/past/', views.PastBookingsAPIView.as_view(), name='past-bookings'),


    path('bookings/<int:prop_id>/', views.PropertyBookingsAPIView.as_view(), name='property-bookings'),


    path('bookings/host/<int:user_id>/', views.HostBookingsAPIView.as_view(), name='host-bookings'),


    path('bookings/<int:id>/', views.BookingAPIView.as_view(), name='single-booking'),


    path('bookings/create/', views.CreateBookingAPIView.as_view(), name='create-booking'),
]
