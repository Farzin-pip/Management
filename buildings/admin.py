from django.contrib import admin
from .models import (
    Building,
    BuildingMembership,
    Unit,
    Ownership,
    Tenancy,
    Floors
)


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'city',
        'type',
        'created_at',
    )

    list_filter = (
        'type',
        'city',
    )

    search_fields = (
        'name',
        'city',
        'address',
    )


@admin.register(BuildingMembership)
class BuildingMembershipAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'building',
        'role',
        'created_at',
    )

    list_filter = (
        'role',
        'building',
    )

    search_fields = (
        'user__phone_number',
        'building__name',
    )


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'building',
        'area',
        'parking_count',
        'storage_number',
        'is_active',
        'created_at',
    )

    list_filter = (
        'building',
        'floor',
        'is_active',
    )

    search_fields = (
        'complex__name',
        'postal_code',
    )


@admin.register(Ownership)
class OwnershipAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'unit',
        'user',
        'start_date',
        'end_date',
        'created_at',
    )

    list_filter = (
        'start_date',
        'end_date',
    )

    search_fields = (
        'user__phone_number',
        'unit__number',
        'unit__complex__name',
    )


@admin.register(Tenancy)
class TenancyAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'unit',
        'user',
        'start_date',
        'end_date',
        'created_at',
    )

    list_filter = (
        'start_date',
        'end_date',
    )

    search_fields = (
        'user__phone_number',
        'unit__number',
        'unit__complex__name',
    )

@admin.register(Floors)
class FloorsAdmin(admin.ModelAdmin):
    fields = (
        'building',
        'floor_count',
        'number',
    )