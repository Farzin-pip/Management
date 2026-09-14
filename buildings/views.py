from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import (
    Building,
    BuildingMembership,
    Floor,
    Unit,
    Ownership,
    Tenancy,
)

from .permissions import IsBuildingManager

from .serializers import (
    BuildingSerializer,
    BuildingMembershipSerializer,
    FloorSerializer,
    UnitSerializer,
    OwnershipSerializer,
    TenancySerializer,
)


class BuildingViewSet(viewsets.ModelViewSet):

    serializer_class = BuildingSerializer

    def get_queryset(self):
        return Building.objects.filter(
            memberships__user=self.request.user
        ).distinct()

    def get_permissions(self):

        if self.action in [
            "update",
            "partial_update",
            "destroy",
        ]:
            return [
                IsAuthenticated(),
                IsBuildingManager(),
            ]

        return [
            IsAuthenticated(),
        ]

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        building = serializer.save()

        BuildingMembership.objects.create(
            user=request.user,
            building=building,
            role=BuildingMembership.Role.MANAGER,
        )

        return Response(
            self.get_serializer(building).data,
            status=status.HTTP_201_CREATED,
        )


class BuildingMembershipViewSet(viewsets.ModelViewSet):

    serializer_class = BuildingMembershipSerializer

    def get_queryset(self):
        return BuildingMembership.objects.filter(
            buildingmembershipsuser=self.request.user,
            buildingmembershipsrole=BuildingMembership.Role.MANAGER,
        ).distinct()

    def get_permissions(self):

        if self.action in [
            "create",
            "update",
            "partial_update",
            "destroy",
        ]:
            return [
                IsAuthenticated(),
                IsBuildingManager(),
            ]

        return [
            IsAuthenticated(),
        ]

    def create(self, request, *args, **kwargs):

        building_id = request.data.get("building")

        if not BuildingMembership.objects.filter(
            user=request.user,
            building_id=building_id,
            role=BuildingMembership.Role.MANAGER,
        ).exists():
            return Response(
                {
                    "detail": "You do not have permission to manage members of this building."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        return super().create(request, *args, **kwargs)


class FloorViewSet(viewsets.ModelViewSet):

    serializer_class = FloorSerializer

    def get_queryset(self):
        return Floor.objects.filter(
            buildingmembershipsuser=self.request.user
        ).distinct()

    def get_permissions(self):

        if self.action in [
            "create",
            "update",
            "partial_update",
            "destroy",
        ]:
            return [
                IsAuthenticated(),
                IsBuildingManager(),
            ]

        return [
            IsAuthenticated(),
        ]

    def create(self, request, *args, **kwargs):

        building_id = request.data.get("building")

        if not BuildingMembership.objects.filter(
            user=request.user,
            building_id=building_id,
            role=BuildingMembership.Role.MANAGER,
        ).exists():
            return Response(
                {
                    "detail": "You do not have permission to create a floor in this building."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        return super().create(request, *args, **kwargs)


class UnitViewSet(viewsets.ModelViewSet):

    serializer_class = UnitSerializer
    def get_queryset(self):
        return Unit.objects.filter(
            floorbuildingmemberships__user=self.request.user
        ).distinct()

    def get_permissions(self):

        if self.action in [
            "create",
            "update",
            "partial_update",
            "destroy",
        ]:
            return [
                IsAuthenticated(),
                IsBuildingManager(),
            ]

        return [
            IsAuthenticated(),
        ]

    def create(self, request, *args, **kwargs):

        floor_id = request.data.get("floor")

        if not BuildingMembership.objects.filter(
            user=request.user,
            buildingfloorsid=floor_id,
            role=BuildingMembership.Role.MANAGER,
        ).exists():
            return Response(
                {
                    "detail": "You do not have permission to create a unit on this floor."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        return super().create(request, *args, **kwargs)


class OwnershipViewSet(viewsets.ModelViewSet):

    serializer_class = OwnershipSerializer

    def get_queryset(self):
        return Ownership.objects.filter(
            unitfloorbuildingmembershipsuser=self.request.user
        ).distinct()

    def get_permissions(self):

        if self.action in [
            "create",
            "update",
            "partial_update",
            "destroy",
        ]:
            return [
                IsAuthenticated(),
                IsBuildingManager(),
            ]

        return [
            IsAuthenticated(),
        ]

    def create(self, request, *args, **kwargs):

        unit_id = request.data.get("unit")

        if not BuildingMembership.objects.filter(
            user=request.user,
            buildingfloorsunits__id=unit_id,
            role=BuildingMembership.Role.MANAGER,
        ).exists():
            return Response(
                {
                    "detail": "You do not have permission to manage this unit."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        return super().create(request, *args, **kwargs)


class TenancyViewSet(viewsets.ModelViewSet):

    serializer_class = TenancySerializer

    def get_queryset(self):
        return Tenancy.objects.filter(
            unitfloorbuildingmembershipsuser=self.request.user
        ).distinct()

    def get_permissions(self):

        if self.action in [
            "create",
            "update",
            "partial_update",
            "destroy",
        ]:
            return [
                IsAuthenticated(),
                IsBuildingManager(),
            ]

        return [
            IsAuthenticated(),
        ]

    def create(self, request, *args, **kwargs):

        unit_id = request.data.get("unit")

        if not BuildingMembership.objects.filter(
            user=request.user,
            buildingfloorsunits__id=unit_id,
            role=BuildingMembership.Role.MANAGER,
        ).exists():
            return Response(
                {
                    "detail": "You do not have permission to manage this unit."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        return super().create(request, *args, **kwargs)