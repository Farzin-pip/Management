from decimal import Decimal
from typing import Any
from django.db.models import QuerySet
from .models import (
    Building,
    BuildingMembership,
    FacilityBookings,
    Tenancy,
    Unit,
    Ownership,
    Floors,
    Facilities,
    Announcements,
    Tickets,
    TicketMessages
)
from django.db.models import Sum
from expenses.models import Invoices, Payment
from datetime import date
from django.db import models


def facility_bookings(facility_id: int) -> QuerySet[FacilityBookings]:
    return FacilityBookings.objects.filter(
        facility_id=facility_id,
        status__in=['pending', 'approved']
    ).select_related('unit_id', 'user_id', 'facility_id')


def facility_booking_by_id(pk: int) -> FacilityBookings:
    return FacilityBookings.objects.get(pk=pk)


def active_tenancy(unit: Unit) -> Tenancy | None:
    return Tenancy.objects.filter(
        unit=unit,
        end_date__isnull=True
    ).select_related('user').first()


def resident_units(user: Any) -> QuerySet[Unit]:
    return Unit.objects.filter(
        tenancies__user=user,
        tenancies__end_date__isnull=True
    ).distinct()


def resident_unit(user: Any, unit_id: int) -> Unit | None:
    return resident_units(user).filter(
        id=unit_id
    ).first()


def resident_buildings(user: Any) -> QuerySet:
    return Unit.objects.filter(
        tenancies__user=user,
        tenancies__end_date__isnull=True,
        building__isnull=False
    ).values_list(
        'building_id',
        flat=True
    ).distinct()


def active_tenancy_for_user(user: Any, unit: Unit) -> Tenancy | None:
    return Tenancy.objects.filter(
        user=user,
        unit=unit,
        end_date__isnull=True
    ).first()


def building_list() -> QuerySet[Building]:
    return Building.objects.all()


def building_by_id(pk: int) -> Building:
    return Building.objects.get(pk=pk)


def building_membership_list() -> QuerySet[BuildingMembership]:
    return BuildingMembership.objects.all()


def building_membership_by_id(pk: int) -> BuildingMembership:
    return BuildingMembership.objects.get(pk=pk)


def unit_list() -> QuerySet[Unit]:
    return Unit.objects.all()


def unit_by_id(pk: int) -> Unit:
    return Unit.objects.filter(pk=pk).first()


def ownership_list() -> QuerySet[Ownership]:
    return Ownership.objects.all()


def ownership_by_id(pk: int) -> Ownership:
    return Ownership.objects.get(pk=pk)


def tenancy_list() -> QuerySet[Tenancy]:
    return Tenancy.objects.all()


def tenancy_by_id(pk: int) -> Tenancy:
    return Tenancy.objects.get(pk=pk)


def floor_list() -> QuerySet[Floors]:
    return Floors.objects.all()


def floor_by_id(pk: int) -> Floors:
    return Floors.objects.get(pk=pk)


def facilities_list() -> QuerySet[Facilities]:
    return Facilities.objects.all()


def facilities_by_id(pk: int) -> Facilities:
    return Facilities.objects.get(pk=pk)


def facility_bookings_list() -> QuerySet[FacilityBookings]:
    return FacilityBookings.objects.all()


def announcement_list() -> QuerySet[Announcements]:
    return Announcements.objects.all()


def announcement_by_id(pk: int) -> Announcements:
    return Announcements.objects.get(pk=pk)


def ticket_list() -> QuerySet[Tickets]:
    return Tickets.objects.all()


def ticket_by_id(pk: int) -> Tickets:
    return Tickets.objects.get(pk=pk)


def ticket_message_list() -> QuerySet[TicketMessages]:
    return TicketMessages.objects.all()


def ticket_message_by_id(pk: int) -> TicketMessages:
    return TicketMessages.objects.get(pk=pk)


def vacant_units_list() -> list[Unit]:
    today = date.today()
    vacant_units = []

    for unit in Unit.objects.all():
        active_tenancy = Tenancy.objects.filter(
            unit=unit,
            start_date__lte=today
        ).filter(
            models.Q(end_date__isnull=True) |
            models.Q(end_date__gte=today)
        ).exists()

        if not active_tenancy:
            vacant_units.append(unit)

    return vacant_units


def active_owner_by_unit(unit: Unit) -> Ownership | None:
    today = date.today()
    return Ownership.objects.filter(
        unit=unit,
        end_date__isnull=True
    ).filter(
        models.Q(start_date__isnull=True) | models.Q(start_date__lte=today)
    ).select_related('user').first()


def unpaid_invoices_by_unit(unit: Unit) -> QuerySet[Invoices]:
    return Invoices.objects.filter(
        unit_id=unit,
        status__in=[
            Invoices.StatusType.UNPAID,
            Invoices.StatusType.PARTIALLY_PAID,
            Invoices.StatusType.OVERDUE
        ]
    ).order_by('due_date')


def successful_payments_total(invoice: Invoices) -> Decimal:
    return Payment.objects.filter(
        invoice_id=invoice,
        status=Payment.Status.SUCCESSFUL
    ).aggregate(total=Sum('amount'))['total'] or 0


