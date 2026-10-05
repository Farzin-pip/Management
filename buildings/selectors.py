from buildings.models import FacilityBookings, Tenancy


def facility_bookings(facility_id):
    return FacilityBookings.objects.filter(
        facility_id=facility_id,
        status__in=['pending', 'approved']
    )


def facility_booking_by_id(pk):
    return FacilityBookings.objects.get(pk=pk)


def active_tenancy(unit):
    return Tenancy.objects.filter(
        unit=unit,
        end_date__isnull=True
    ).select_related('user').first()