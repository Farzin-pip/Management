from rest_framework import serializers
from .models import Building, BuildingMembership, Floors, Unit, Ownership, Tenancy, Facilities, FacilityBookings, Announcements, Tickets, TicketMessages
from .component import check_facility_booking


class UnitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Unit
        fields = '__all__'


class OwnershipSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ownership
        fields = '__all__'


class TenancySerializer(serializers.ModelSerializer):

    class Meta:
        model = Tenancy
        fields = '__all__'


class BuildingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Building
        fields = '__all__'


class BuildingMembershipSerializer(serializers.ModelSerializer):

    class Meta:
        model = BuildingMembership
        fields = '__all__'


class FloorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Floors
        fields = '__all__'


class FacilitiesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Facilities
        fields = '__all__'


class FacilityBookingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = FacilityBookings
        fields = '__all__'


class AnnouncementsSerializer(serializers.ModelSerializer):

    class Meta:
        model =  Announcements
        fields = '__all__'


class TicketsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tickets
        fields = '__all__'


class TicketMessagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = TicketMessages
        fields = '__all__'


class VacantUnitOverdueChargeSerializer(serializers.Serializer):
    invoice_id = serializers.IntegerField()
    due_date = serializers.DateField()
    monthly_charge = serializers.DecimalField(max_digits=12, decimal_places=2)
    paid_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    overdue_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    late_months = serializers.IntegerField()
    penalty = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_due = serializers.DecimalField(max_digits=12, decimal_places=2)


class VacantUnitReportSerializer(serializers.Serializer):
    unit_number = serializers.IntegerField()
    owner_name = serializers.CharField(allow_null=True)
    owner_phone = serializers.CharField(allow_null=True)
    total_due = serializers.DecimalField(max_digits=12, decimal_places=2)


class VacantFloorReportSerializer(serializers.Serializer):
    floor = serializers.IntegerField()
    vacant_units_count = serializers.IntegerField()
    units = VacantUnitReportSerializer(many=True)
