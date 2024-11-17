from django.urls import path
from .views import *

urlpatterns = [
    path('', BookingsList.as_view(), name='bookings-list'),
    path('upcoming/', UpcomingBookings.as_view(), name='upcoming-bookings'),
    path('new/<int:prop_id>/', BookingsNew.as_view(), name='bookings-new'),
    path('<int:id>/', BookingsOne.as_view(), name='bookings-one'),
]
