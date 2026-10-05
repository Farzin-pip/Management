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

    def validate(self, data):
        facility_id = data.get('facility_id', self.instance.facility_id if self.instance else None)
        start_time = data.get('start_time', self.instance.start_time if self.instance else None)
        end_time = data.get('end_time', self.instance.end_time if self.instance else None)

        if start_time >= end_time:
            raise serializers.ValidationError(
                {'message': 'End time must be after start time!'}
            )

        booking_id = self.instance.pk if self.instance else None

        booking = check_facility_booking(
            facility_id,
            start_time,
            end_time,
            booking_id
        )

        if booking:
            raise serializers.ValidationError(
                {
                    'message': f'This facility is already booked by unit '
                               f'{booking.unit_id.number}!'
                }
            )

        return data


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
