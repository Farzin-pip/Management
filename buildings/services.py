from buildings.models import FacilityBookings
from .selectors import facility_bookings, active_tenancy
from datetime import timedelta



def create_facility_booking(data):

    facility_id = data['facility_id']
    start_time = data['start_time']
    end_time = data['end_time']

    if start_time >= end_time:
        raise ValueError('End time must be after start time!')

    bookings = facility_bookings(facility_id)

    for booking in bookings:
        if (
                start_time < booking.end_time + timedelta(minutes=30)
                and end_time > booking.start_time - timedelta(minutes=30)
        ):
            tenancy = active_tenancy(booking.unit_id)

            if tenancy:
                resident_name = (
                    f'{tenancy.user.first_name} '
                    f'{tenancy.user.last_name}'
                )

                resident_phone = tenancy.user.phone_number

                raise ValueError(
                    f'This facility is already booked by unit '
                    f'{booking.unit_id.number} by resident '
                    f'{resident_name} ({resident_phone})!'
                )

            raise ValueError(
                f'This facility is already booked by unit '
                f'{booking.unit_id.number}!'
            )

    return FacilityBookings.objects.create(**data)


def update_facility_booking(booking, data):
    facility_id = data.get('facility_id', booking.facility_id)
    start_time = data.get('start_time', booking.start_time)
    end_time = data.get('end_time', booking.end_time)

    if not start_time or not end_time:
        raise ValueError('Start time and end time are required!')

    if start_time >= end_time:
        raise ValueError('End time must be after start time!')

    bookings = facility_bookings(facility_id).exclude(
        pk=booking.pk
    )

    for old_booking in bookings:
        if (
            start_time < old_booking.end_time + timedelta(minutes=30)
            and end_time > old_booking.start_time - timedelta(minutes=30)
        ):
            tenancy = active_tenancy(old_booking.unit_id)

            if tenancy:
                resident_name = (
                    f'{tenancy.user.first_name} '
                    f'{tenancy.user.last_name}'
                )

                resident_phone = tenancy.user.phone_number

                raise ValueError(
                    f'This facility is already booked by unit '
                    f'{old_booking.unit_id.number}. '
                    f'Resident: {resident_name}, '
                    f'Phone: {resident_phone}'
                )

            raise ValueError(
                f'This facility is already booked by unit '
                f'{old_booking.unit_id.number}!'
            )

    if 'facility_id' in data:
        booking.facility_id = data['facility_id']

    if 'unit_id' in data:
        booking.unit_id = data['unit_id']

    if 'user_id' in data:
        booking.user_id = data['user_id']

    if 'start_time' in data:
        booking.start_time = data['start_time']

    if 'end_time' in data:
        booking.end_time = data['end_time']

    if 'fee_amount' in data:
        booking.fee_amount = data['fee_amount']

    if 'status' in data:
        booking.status = data['status']

    booking.save()

    return booking