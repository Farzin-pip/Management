from datetime import timedelta
from .models import FacilityBookings
from .selectors import facility_bookings


def check_facility_booking(
    facility_id,
    start_time,
    end_time,
    booking_id=None
):

    bookings = facility_bookings(facility_id)

    if booking_id:
        bookings = bookings.exclude(pk=booking_id)

    for booking in bookings:

        old_start = booking.start_time
        old_end = booking.end_time

        if (
            start_time < old_end + timedelta(minutes=30)
            and end_time > old_start - timedelta(minutes=30)
        ):
            return booking

    return None