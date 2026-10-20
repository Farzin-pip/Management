from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from .selectors import user_list, user_by_id
from .services import create_user, update_user, delete_user
from .serializers import UserSerializer
from .models import User


class UserView(APIView):
    def get(self, request):
        users = user_list()
        ser_data = UserSerializer(users, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            user = create_user(request.data)
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk: int):
        try:
            user = user_by_id(pk)
        except User.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            user = update_user(user, request.data)
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk: int):
        try:
            user = user_by_id(pk)
        except User.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        delete_user(user)
        return Response({'message': 'User Deleted!'}, status=status.HTTP_200_OK)