from datetime import timedelta
from .models import FacilityBookings


def check_facility_booking(
    facility_id,
    start_time,
    end_time,
    booking_id=None
):

    bookings = FacilityBookings.objects.filter(
        facility_id=facility_id,
        status__in=['pending', 'approved']
    )

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