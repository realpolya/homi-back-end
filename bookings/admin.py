from django.contrib import admin
from .models import Booking

class BookingAdmin(admin.ModelAdmin):
    readonly_fields = ('total_price',)

admin.site.register(Booking, BookingAdmin)

