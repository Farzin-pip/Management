from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    BuildingViewSet,
    BuildingMembershipViewSet,
    FloorViewSet,
    UnitViewSet,
    OwnershipViewSet,
    TenancyViewSet,
)


router = DefaultRouter()

router.register(
    "buildings",
    BuildingViewSet,
    basename="building"
)

router.register(
    "memberships",
    BuildingMembershipViewSet,
    basename="building-membership"
)

router.register(
    "floors",
    FloorViewSet,
    basename="floor"
)

router.register(
    "units",
    UnitViewSet,
    basename="unit"
)

router.register(
    "ownerships",
    OwnershipViewSet,
    basename="ownership"
)

router.register(
    "tenancies",
    TenancyViewSet,
    basename="tenancy"
)


urlpatterns = [
    path("", include(router.urls)),
]