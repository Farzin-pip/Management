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
