from rest_framework import serializers
from .models import Building, BuildingMembership, Floor, Unit, Ownership, Tenancy


class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = ["id", "name", "address", "floor_count", "unit_count", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class BuildingMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildingMembership
        fields = ["id", "user", "building", "role", "created_at"]
        read_only_fields = ["id", "created_at"]


class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = ["id", "building", "number", "created_at"]
        read_only_fields = ["id", "created_at"]


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ["id", "floor", "number", "postal_code", "area", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class OwnershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ownership
        fields = ["id", "unit", "user", "start_date", "end_date", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate(self, attrs):
        start_date = attrs.get("start_date", getattr(self.instance, "start_date", None))
        end_date = attrs.get("end_date", getattr(self.instance, "end_date", None))

        if end_date and start_date and end_date < start_date:
            raise serializers.ValidationError({"end_date": "End date must be greater than or equal to start date."})

        unit = attrs.get("unit", getattr(self.instance, "unit", None))
        user = attrs.get("user", getattr(self.instance, "user", None))

        if unit and user:
            building = unit.floor.building
            exists = BuildingMembership.objects.filter(
                user=user,
                building=building,
                role=BuildingMembership.Role.OWNER
            ).exists()

            if not exists:
                raise serializers.ValidationError({"user": "User must have the owner role in this building."})

        return attrs


class TenancySerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenancy
        fields = ["id", "unit", "user", "start_date", "end_date", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate(self, attrs):
        start_date = attrs.get("start_date", getattr(self.instance, "start_date", None))
        end_date = attrs.get("end_date", getattr(self.instance, "end_date", None))

        if end_date and start_date and end_date < start_date:
            raise serializers.ValidationError({"end_date": "End date must be greater than or equal to start date."})

        unit = attrs.get("unit", getattr(self.instance, "unit", None))
        user = attrs.get("user", getattr(self.instance, "user", None))

        if unit and user:
            building = unit.floor.building
            exists = BuildingMembership.objects.filter(
                user=user,
                building=building,
                role=BuildingMembership.Role.RESIDENT
            ).exists()

            if not exists:
                raise serializers.ValidationError({"user": "User must have the resident role in this building."})

        return attrs