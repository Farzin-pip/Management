from rest_framework import serializers
from .models import Building




class BuildingSerializers(serializers.ModelSerializer):

    class META:
        model = Building
        fields = [
            "id",
            "name",
            "address",
            "floor_count"
            "unit_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]