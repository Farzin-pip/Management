from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.request import Request

from utils.utils import send_otp
from .selectors import user_list, user_by_id
from .services import create_user, update_user, delete_user, login_user, logout_user, register_user
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, LogoutSerializer, SendOtpSerializer
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


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = register_user(serializer.validated_data)
            return Response(
                {
                    "message": "ثبت‌نام با موفقیت انجام شد.",
                    "user": {
                        "id": user.pk,
                        "phone_number": user.phone_number,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "role": user.role,
                    },
                }, status=status.HTTP_201_CREATED,)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            try:
                tokens = login_user(
                    serializer.validated_data["phone_number"],
                    serializer.validated_data["password"],
                )
                return Response(tokens, status=status.HTTP_200_OK)

            except AuthenticationFailed as e:
                return Response({"error": str(e.detail)}, status=status.HTTP_401_UNAUTHORIZED,)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        serializer = LogoutSerializer(data=request.data)

        if serializer.is_valid():
            try:
                logout_user(serializer.validated_data["refresh"], request.user)
                return Response({"message": "خروج با موفقیت انجام شد."}, status=status.HTTP_205_RESET_CONTENT,)

            except AuthenticationFailed as e:
                return Response({"error": str(e.detail)}, status=status.HTTP_400_BAD_REQUEST,)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendOtpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SendOtpSerializer(data=request.data)

        if serializer.is_valid():
            result = send_otp(serializer.validated_data["phone_number"])

            if result:
                return Response({"message": "کد تأیید ارسال شد."}, status=status.HTTP_200_OK,)

            return Response({"error": "ارسال پیامک ناموفق بود."}, status=status.HTTP_502_BAD_GATEWAY,)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)