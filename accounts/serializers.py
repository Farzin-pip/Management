from .models import User
from rest_framework import serializers
from accounts.selectors import get_user_by_phone, get_otp_by_phone
from datetime import timedelta
from django.utils import timezone

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'phone_number',
            'first_name',
            'last_name',
            'role',
            'password',
            'is_active',
            'is_staff',
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class SendOtpSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)

    def validate_phone_number(self, value: str) -> str:
        if len(value) != 11 or not value.startswith("09") or not value.isdigit():
            raise serializers.ValidationError("شماره موبایل معتبر نیست.")

        if get_user_by_phone(value):
            raise serializers.ValidationError("این شماره موبایل قبلاً ثبت‌نام کرده است.")

        return value


class RegisterSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    password = serializers.CharField(min_length=8, write_only=True)
    otp = serializers.IntegerField()

    def validate_phone_number(self, value: str) -> str:
        if len(value) != 11 or not value.startswith("09") or not value.isdigit():
            raise serializers.ValidationError("شماره موبایل معتبر نیست.")

        if get_user_by_phone(value):
            raise serializers.ValidationError("این شماره قبلاً ثبت‌نام کرده است.")

        return value

    def validate(self, attrs: dict) -> dict:
        otp = get_otp_by_phone(attrs["phone_number"])

        if otp is None or otp.code != attrs["otp"]:
            raise serializers.ValidationError({"otp": "کد تأیید اشتباه است."})

        if timezone.now() - otp.created_at > timedelta(minutes=2):
            raise serializers.ValidationError({"otp": "کد تأیید منقضی شده است."})

        return attrs


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)
    password = serializers.CharField(write_only=True)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()