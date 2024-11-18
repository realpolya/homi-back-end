from .models import Booking

def get_availability(listing, check_in, check_out, current_booking=None):
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

    if current_booking:
        print("working with current booking")
        overlapping_bookings = overlapping_bookings.exclude(pk=current_booking.pk)
    
    if len(overlapping_bookings) != 0:
        return False
    
    return True