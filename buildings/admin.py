from django.contrib import admin

from utils.utils import ReadOnlyModelAdmin
from .models import (
    Building, BuildingMembership, Floors, Unit, Ownership, Tenancy,
    Facilities, FacilityBookings, Announcements, Tickets, TicketMessages
)


@admin.register(Building)
class BuildingAdmin(ReadOnlyModelAdmin):
    list_display = ['id', 'name', 'city', 'type', 'unit_count', 'created_at']
    search_fields = ['name', 'city']
    list_filter = ['type', 'city']


@admin.register(BuildingMembership)
class BuildingMembershipAdmin(ReadOnlyModelAdmin):
    list_display = ['id', 'user', 'building', 'role', 'created_at']
    list_filter = ['role']
    search_fields = ['user__phone_number', 'building__name']


@admin.register(Floors)
class FloorsAdmin(ReadOnlyModelAdmin):
    list_display = ['id', 'building', 'number', 'floor_count']
    list_filter = ['building']


@admin.register(Unit)
class UnitAdmin(ReadOnlyModelAdmin):
    list_display = ['id', 'building', 'floor', 'number', 'area', 'is_active']
    list_filter = ['building', 'floor', 'is_active']
    search_fields = ['building__name', 'postal_code']


@admin.register(Ownership)
class OwnershipAdmin(ReadOnlyModelAdmin):
    list_display = ['id', 'unit', 'user', 'start_date', 'end_date', 'created_at']
    list_filter = ['start_date', 'end_date']
    search_fields = ['user__phone_number', 'user__first_name', 'user__last_name']


@admin.register(Tenancy)
class TenancyAdmin(ReadOnlyModelAdmin):
    list_display = ['id', 'unit', 'user', 'start_date', 'end_date', 'created_at']
    list_filter = ['start_date', 'end_date']
    search_fields = ['user__phone_number', 'user__first_name', 'user__last_name']


@admin.register(Facilities)
class FacilitiesAdmin(ReadOnlyModelAdmin):
    list_display = ['id', 'name', 'building_id', 'capacity', 'hourly_rate']
    list_filter = ['name', 'building_id']
    search_fields = ['name']


@admin.register(FacilityBookings)
class FacilityBookingsAdmin(ReadOnlyModelAdmin):
    list_display = [
        'id', 'facility_id', 'unit_id', 'user_id',
        'start_time', 'end_time', 'status', 'payment_type', 'is_paid'
    ]
    list_filter = ['status', 'payment_type', 'is_paid']
    search_fields = ['user_id__phone_number']


@admin.register(Announcements)
class AnnouncementsAdmin(ReadOnlyModelAdmin):
    list_display = ['id', 'title', 'building_id', 'is_pinned', 'published_at']
    list_filter = ['is_pinned', 'building_id']
    search_fields = ['title', 'body']


@admin.register(Tickets)
class TicketsAdmin(ReadOnlyModelAdmin):
    list_display = [
        'id', 'subject', 'building_id', 'unit_id',
        'user_id', 'status', 'priority'
    ]
    list_filter = ['status', 'priority', 'building_id']
    search_fields = ['subject', 'user_id__phone_number']


@admin.register(TicketMessages)
class TicketMessagesAdmin(ReadOnlyModelAdmin):
    list_display = ['id', 'ticket']
    search_fields = ['ticket__subject', 'description']
