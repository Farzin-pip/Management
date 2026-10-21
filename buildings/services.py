from buildings.models import FacilityBookings, Building, BuildingMembership, Unit, Ownership, Tenancy, Floors, \
    Facilities, Announcements, Tickets, TicketMessages
from expenses.models import InvoicePenalty
from expenses.selectors import successful_booking_payment, booking_payment_exists
from .selectors import facility_bookings, active_tenancy
from datetime import timedelta
from typing import Any
from decimal import Decimal
from datetime import date
from .selectors import (
    vacant_units_list, active_owner_by_unit,
    unpaid_invoices_by_unit, successful_payments_total
)
from expenses.services import save_invoice_penalties, add_booking_fee_to_invoice, cancel_booking_invoice_item
from django.db.models import Sum


def create_building(data: dict[str, Any]) -> Building:
    return Building.objects.create(**data)


def update_building(building: Building, data: dict[str, Any]) -> Building:
    for key, value in data.items():
        setattr(building, key, value)
    building.save()
    return building


def delete_building(building: Building) -> None:
    building.delete()


def create_building_membership(data: dict[str, Any]) -> BuildingMembership:
    return BuildingMembership.objects.create(**data)


def update_building_membership(building_membership: BuildingMembership, data: dict[str, Any]) -> BuildingMembership:
    for key, value in data.items():
        setattr(building_membership, key, value)
    building_membership.save()
    return building_membership


def delete_building_membership(building_membership: BuildingMembership) -> None:
    building_membership.delete()


def create_unit(data: dict[str, Any]) -> Unit:
    return Unit.objects.create(**data)


def update_unit(unit: Unit, data: dict[str, Any]) -> Unit:
    for key, value in data.items():
        setattr(unit, key, value)
    unit.save()
    return unit


def delete_unit(unit: Unit) -> None:
    unit.delete()


def create_ownership(data: dict[str, Any]) -> Ownership:
    return Ownership.objects.create(**data)


def update_ownership(ownership: Ownership, data: dict[str, Any]) -> Ownership:
    for key, value in data.items():
        setattr(ownership, key, value)
    ownership.save()
    return ownership


def delete_ownership(ownership: Ownership) -> None:
    ownership.delete()


def create_tenancy(data: dict[str, Any]) -> Tenancy:
    return Tenancy.objects.create(**data)


def update_tenancy(tenancy: Tenancy, data: dict[str, Any]):
    for key, value in data.items():
        setattr(tenancy, key, value)
    tenancy.save()
    return tenancy


def delete_tenancy(tenancy: Tenancy) -> None:
    tenancy.delete()


def create_floor(data: dict[str, Any]) -> Floors:
    return Floors.objects.create(**data)

def update_floor(floor: Floors, data: dict[str, Any]) -> Floors:
    for key, value in data.items():
        setattr(floor, key, value)
    floor.save()
    return floor


def delete_floor(floor: Floors) -> None:
    floor.delete()


def create_facilities(data: dict[str, Any]) -> Facilities:
    return Facilities.objects.create(**data)


def update_facilities(facilities: Facilities, data: dict[str, Any]) -> Facilities:
    for key, value in data.items():
        setattr(facilities, key, value)
    facilities.save()
    return facilities


def delete_facilities(facilities: Facilities) -> None:
    facilities.delete()


def create_announcement(data: dict[str, Any]) -> Announcements:
    return Announcements.objects.create(**data)


def update_announcement(announcement: Announcements, data: dict[str, Any]) -> Announcements:
    for key, value in data.items():
        setattr(announcement, key, value)
    announcement.save()
    return announcement


def delete_announcement(announcement: Announcements) -> None:
    announcement.delete()


def create_ticket(data: dict[str, Any]) -> Tickets:
    return Tickets.objects.create(**data)


def update_ticket(ticket: Tickets, data: dict[str, Any]) -> Tickets:
    for key, value in data.items():
        setattr(ticket, key, value)
    ticket.save()
    return ticket


def delete_ticket(ticket: Tickets) -> None:
    ticket.delete()


def create_ticket_message(data: dict[str, Any]) -> TicketMessages:
    return TicketMessages.objects.create(**data)


def update_ticket_message(ticket_message: TicketMessages, data: dict[str, Any]) -> TicketMessages:
    for key, value in data.items():
        setattr(ticket_message, key, value)
    ticket_message.save()
    return ticket_message


def delete_ticket_message(ticket_message: TicketMessages) -> None:
    ticket_message.delete()


def create_facility_booking(data: dict[str, Any]) -> FacilityBookings:
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

    booking = FacilityBookings.objects.create(**data)

    if booking.status == FacilityBookings.StatusType.APPROVED:
        add_booking_fee_to_invoice(booking)

    return booking


def update_facility_booking(booking: FacilityBookings, data: dict[str, Any]) -> FacilityBookings:
    facility_id = data.get('facility_id', booking.facility_id)
    start_time = data.get('start_time', booking.start_time)
    end_time = data.get('end_time', booking.end_time)
    old_status = booking.status
    old_payment_type = booking.payment_type
    new_payment_type = data.get('payment_type', booking.payment_type)

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

    cancelling = (
        old_status == FacilityBookings.StatusType.APPROVED
        and data.get('status') == FacilityBookings.StatusType.CANCELLED
    )

    changing_to_instant = (
        old_payment_type == FacilityBookings.PaymentType.INVOICE
        and new_payment_type == FacilityBookings.PaymentType.INSTANT
    )

    changing_payment_type = old_payment_type != new_payment_type

    if changing_payment_type and booking_payment_exists(booking):
        raise ValueError(
            'This booking has a pending or successful payment. '
            'Resolve the payment first.'
        )

    if 'fee_amount' in data:
        new_fee_amount = Decimal(str(data['fee_amount']))

        if (
                new_fee_amount != booking.fee_amount
                and (
                booking.is_paid
                or successful_booking_payment(booking)
        )
        ):
            raise ValueError(
                'This booking has a successful payment. '
                'The booking amount cannot be changed.'
            )

    if cancelling:
        if successful_booking_payment(booking):
            raise ValueError(
                'This booking has a successful payment. '
                'The refund must be handled first.'
            )

        cancel_booking_invoice_item(booking)

    elif changing_to_instant:
        cancel_booking_invoice_item(booking)

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

    if 'payment_type' in data:
        booking.payment_type = data['payment_type']

    booking.save()

    if not cancelling and booking.status == FacilityBookings.StatusType.APPROVED:
        add_booking_fee_to_invoice(booking)

    return booking


def delete_facility_booking(facility_booking: FacilityBookings) -> None:
    facility_booking.delete()


def vacant_units_overdue_report() -> list[dict]:
    today = date.today()
    units = []

    for unit in vacant_units_list():
        owner = active_owner_by_unit(unit)

        total_overdue = Decimal('0.00')
        total_penalty = Decimal('0.00')

        for invoice in unpaid_invoices_by_unit(unit):
            if invoice.due_date >= today:
                continue

            paid_amount = Decimal(str(successful_payments_total(invoice)))
            remaining_amount = max(
                Decimal('0.00'),
                invoice.total_amount - paid_amount
            )

            if remaining_amount <= 0:
                continue

            late_months = (
                (today.year - invoice.due_date.year) * 12
                + today.month - invoice.due_date.month
            )

            if today.day < invoice.due_date.day:
                late_months -= 1

            late_months = max(0, late_months)

            save_invoice_penalties(invoice, late_months)

            penalty = InvoicePenalty.objects.filter(
                invoice=invoice
            ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

            total_overdue += remaining_amount
            total_penalty += penalty

        units.append({
            'unit_number': unit.number,
            'owner_name': f'{owner.user.first_name} {owner.user.last_name}'.strip() if owner else None,
            'owner_phone': owner.user.phone_number if owner else None,
            'total_due': total_overdue + total_penalty
        })

    return units