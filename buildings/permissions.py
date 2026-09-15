from rest_framework.permissions import BasePermission
from .models import Building, BuildingMembership


def get_building_from_object(obj):
    if isinstance(obj, Building):
        return obj

    if hasattr(obj, "building_id"):
        return obj.building

    if hasattr(obj, "floor_id"):
        return obj.floor.building

    if hasattr(obj, "unit_id"):
        return obj.unit.floor.building

    return None


def is_building_manager(user, building):
    if not building:
        return False

    return BuildingMembership.objects.filter(
        user=user,
        building=building,
        role=BuildingMembership.Role.MANAGER
    ).exists()


class IsBuildingManager(BasePermission):
    def has_object_permission(self, request, view, obj):
        building = get_building_from_object(obj)
        return is_building_manager(request.user, building)