from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from .models import User, UserToken
from .serializers import UserSerializer
import secrets
from django.utils import timezone
from accounts.models import OtpCode
from django.contrib.auth import get_user_model
from datetime import datetime, timezone as dt_timezone


def create_user(data: dict):
    ser_data = UserSerializer(data=data)
    ser_data.is_valid(raise_exception=True)
    return ser_data.save()


def update_user(user: User, data: dict):
    ser_data = UserSerializer(user, data=data, partial=True)
    ser_data.is_valid(raise_exception=True)
    return ser_data.save()


def delete_user(user: User):
    user.delete()


def generate_otp_code() -> int:
    return secrets.randbelow(9000) + 1000


def create_otp(phone_number: str) -> int:
    code = generate_otp_code()

    OtpCode.objects.update_or_create(
        phone_number=phone_number,
        defaults={
            "code": code,
            "created_at": timezone.now(),
        },
    )

    return code


def register_user(validated_data: dict) -> User:
    user = User.objects.create_user(
        phone_number=validated_data["phone_number"],
        first_name=validated_data["first_name"],
        last_name=validated_data["last_name"],
        password=validated_data["password"],
        role="RESIDENT",
    )

    OtpCode.objects.filter(
        phone_number=validated_data["phone_number"]
    ).delete()

    return user


def logout_user(refresh_token: str, user: User) -> None:
    try:
        token = RefreshToken(refresh_token)

        if str(token["user_id"]) != str(user.pk):
            raise AuthenticationFailed("این توکن متعلق به کاربر فعلی نیست.")

        token.blacklist()

    except TokenError:
        raise AuthenticationFailed("توکن نامعتبر است یا قبلاً باطل شده است.")


User = get_user_model()
def save_user_tokens(
    user: User,
    access_token: str,
    refresh_token: str,
) -> UserToken:
    access = AccessToken(access_token)
    refresh = RefreshToken(refresh_token)

    token, _ = UserToken.objects.update_or_create(
        user=user,
        defaults={
            'access_token': access_token,
            'refresh_token': refresh_token,
            'access_expires_at': datetime.fromtimestamp(
                access['exp'], tz=dt_timezone.utc
            ),
            'refresh_expires_at': datetime.fromtimestamp(
                refresh['exp'], tz=dt_timezone.utc
            ),
        },
    )
    return token


def login_user(phone_number: str, password: str) -> dict:
    user = authenticate(
        username=phone_number,
        password=password,
    )

    if user is None or not user.is_active:
        raise AuthenticationFailed("شماره موبایل یا رمز عبور اشتباه است.")

    refresh = RefreshToken.for_user(user)
    access = refresh.access_token

    save_user_tokens(user=user, access_token=str(access), refresh_token=str(refresh),)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
