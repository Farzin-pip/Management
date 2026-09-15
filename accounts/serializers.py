from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import OtpCode


User = get_user_model()


class RegisterOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)

    def validate_phone_number(self, value):
        if not value.isdigit() or len(value) != 11 or not value.startswith("09"):
            raise serializers.ValidationError(
                "Enter a valid phone number."
            )

        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError(
                "User already exists."
            )

        return value


class RegisterVerifyOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)
    code = serializers.CharField(max_length=4)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    password = serializers.CharField(
        min_length=8,
        write_only=True,
    )

    def validate(self, attrs):
        otp = OtpCode.objects.filter(
            phone_number=attrs["phone_number"],
            code=int(attrs["code"]),
        ).first()

        if not otp:
            raise serializers.ValidationError(
                {"code": "Invalid OTP code."}
            )

        attrs["otp"] = otp
        return attrs


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        from rest_framework_simplejwt.tokens import RefreshToken

        self.token = RefreshToken(attrs["refresh"])
        return attrs

    def save(self, **kwargs):
        self.token.blacklist()