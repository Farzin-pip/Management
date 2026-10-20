from .models import User
from .serializers import UserSerializer


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