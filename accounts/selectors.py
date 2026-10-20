from django.db.models import QuerySet
from .models import User


def user_list() -> QuerySet[User]:
    return User.objects.all()


def user_by_id(pk: int) -> User:
    return User.objects.get(pk=pk)