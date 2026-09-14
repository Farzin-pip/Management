from django.db import models
from django.conf import settings


class Building(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=2000)
    floor_count = models.PositiveIntegerField(default=0)
    unit_count = models.PositiveIntegerField(default=0)


    def __str__(self):
        return self.name


class BuildingMembership(models.Model):

    class Role(models.TextChoices):
        MANAGER = 'manager'
        OWNER = 'owner'
        RESIDENT = 'resident'
        STAFF = 'staff'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='building_membership')
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='memberships')
    role = models.CharField(max_length=20, choices=Role.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}|{self.building}|{self.role}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "building", "role"],
                name="unique_user_building_role"
            )
        ]


class Floor(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='floors')
    number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.building.name} -Floor:{self.number}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["building", "number"],
                name="unique_floor_per_building"
            )
        ]


class Unit(models.Model):
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name="units")
    number = models.IntegerField()
    past_address = models.CharField(max_length=100, unique=True, null=True, blank=True)
    area = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.floor.building.name} -Unit:{self.number}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["floor", "number"],
                name="unique_unit_per_floor"
            )
        ]


class Ownership(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='owners')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_units')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-start_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["unit"],
                condition=models.Q(end_date__isnull=True),
                name="unique_active_ownership_per_unit"
            )
        ]


class Tenancy(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='tenancies')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rental_history')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-start_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["unit"],
                condition=models.Q(end_date__isnull=True),
                name="unique_active_tenancy_per_unit"
            )
        ]