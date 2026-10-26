from django.db.models import QuerySet
from .models import User, OtpCode, UserToken


def user_list() -> QuerySet[User]:
    return User.objects.all()


def user_by_id(pk: int) -> User:
    return User.objects.get(pk=pk)


def get_user_by_phone(phone_number: str) -> User | None:
    return User.objects.filter(phone_number=phone_number).first()


def get_otp_by_phone(phone_number: str) -> OtpCode | None:
    return OtpCode.objects.filter(phone_number=phone_number).first()


def get_user_token(user: User) -> UserToken | None:
    return UserToken.objects.filter(user=user).first()