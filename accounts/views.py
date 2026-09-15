from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (LogoutSerializer, RegisterOTPSerializer, RegisterVerifyOTPSerializer)
from utils import create_otp, send_otp_code


User = get_user_model()


class RegisterRequestOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data["phone_number"]
        code = create_otp(phone)

        send_otp_code(phone, code)

        return Response(
            {"message": "OTP sent successfully."},
            status=status.HTTP_200_OK,
        )


class RegisterVerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterVerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        user = User.objects.create_user(
            phone_number=data["phone_number"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            password=data["password"],
        )

        data["otp"].delete()

        return Response(
            {"user_id": user.id},
            status=status.HTTP_201_CREATED,
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Logout successful."},
            status=status.HTTP_200_OK,
        )
