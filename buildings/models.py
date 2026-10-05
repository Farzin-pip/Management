from django.db import models
from django.conf import settings


class Building(models.Model):

    class BuildingType(models.TextChoices):
        RESIDENTIAL = 'residential'
        COMMERCIAL = 'commercial'
        OFFICE = 'office'
        INDUSTRIAL = 'industrial'

    name = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=2000, null=True, blank=True)
    type = models.CharField(max_length=20, choices=BuildingType.choices, null=True, blank=True)
    unit_count = models.IntegerField(default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    bank_account_number = models.CharField(max_length=30, blank=True, null=True)
    iban = models.CharField(max_length=34, blank=True, null=True)


    def __str__(self):
        return self.name


class BuildingMembership(models.Model):

    class Role(models.TextChoices):
        MANAGER = 'manager'
        OWNER = 'owner'
        RESIDENT = 'resident'
        STAFF = 'staff'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='building_membership',
                             null=True, blank=True)
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='memberships', null=True, blank=True)
    role = models.CharField(max_length=20, choices=Role.choices, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.user}|{self.building}|{self.role}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "building", "role"],
                name="unique_user_building_role"
            )
        ]

class Floors(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, null=True, blank=True)
    floor_count = models.IntegerField(default=0, null=True, blank=True)
    number = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return f"{self.number}-{self.building}"


class Unit(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name="units", null=True, blank=True)
    floor = models.ForeignKey(Floors, on_delete=models.CASCADE, related_name="unit_floor", null=True, blank=True)
    number = models.IntegerField(null=True, blank=True)
    postal_code = models.CharField(max_length=100, unique=True, null=True, blank=True)
    area = models.IntegerField(null=True, blank=True)
    parking_count = models.PositiveIntegerField(default=0, null=True, blank=True)
    storage_number = models.PositiveIntegerField(null=True, blank=True)
    ownership = models.ForeignKey('Ownership', on_delete=models.CASCADE, related_name="unit_ownership", null=True, blank=True)
    tenancy = models.ForeignKey('Tenancy', on_delete=models.CASCADE, related_name="unit_tenancy", null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.number}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["building", "floor", "number"],
                name="unique_unit_per_floor"
            )
        ]


class Ownership(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='owners', null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_units', null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.user.last_name}"

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
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='tenancies', null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rental_history', null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ["-start_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["unit"],
                condition=models.Q(end_date__isnull=True),
                name="unique_active_tenancy_per_unit"
            )
        ]


class Facilities(models.Model):

    class FacilityType(models.TextChoices):
        POOL = 'pool'
        FUNCTION_HALL = 'function_hall'
        ROOF_GARDEN = 'roof_garden'

    building_id = models.ForeignKey(Building, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, choices=FacilityType.choices)
    capacity = models.IntegerField()
    hourly_rate = models.FloatField()

    def __str__(self):
        return self.name


class FacilityBookings(models.Model):

    class StatusType(models.TextChoices):
        CANCELLED = 'canceled'
        REJECTED = 'rejected'
        APPROVED = 'approved'
        PENDING = 'pending'

    facility_id = models.ForeignKey(Facilities, on_delete=models.CASCADE)
    unit_id = models.ForeignKey(Unit, on_delete=models.CASCADE)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    fee_amount = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=30, choices=StatusType.choices)

    def __str__(self):
        return str(self.facility_id)


class Announcements(models.Model):
    building_id = models.ForeignKey(Building, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    is_pinned = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title


class Tickets(models.Model):

    class PriorityType(models.TextChoices):
        LOW = 'low'
        MEDIUM = 'medium'
        HIGH = 'high'
        CRITICAL = 'critical'

    class StatusType(models.TextChoices):
        OPEN = 'open'
        IN_PROGRESS = 'in_progress'
        RESOLVED = 'resolved'
        CLOSED = 'closed'

    building_id = models.ForeignKey(Building, on_delete=models.CASCADE)
    unit_id = models.ForeignKey(Unit, on_delete=models.CASCADE)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject = models.CharField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(choices=StatusType.choices)
    priority = models.CharField(choices=PriorityType.choices)

    def __str__(self):
        return self.subject


class TicketMessages(models.Model):
    ticket = models.ForeignKey(Tickets, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.ticket)



