from django.urls import path
from .views import *

urlpatterns = [
    path('', BookingsList.as_view(), name='bookings-list'),
    path('upcoming/', UpcomingBookings.as_view(), name='upcoming-bookings'),
    path('prev/', PreviousBookings.as_view(), name='previous-bookings'),
    path('new/<int:prop_id>/', BookingsNew.as_view(), name='bookings-new'),
    path('<int:id>/', BookingsOne.as_view(), name='bookings-one'),
    path('host/', BookingsHost.as_view(), name='bookings-host'),
    path('prop/<int:prop_id>/', BookingsProperty.as_view(), name='bookings-property'),
]

