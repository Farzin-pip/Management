from django.urls import path
from .views import (LogoutView, RegisterRequestOTPView, RegisterVerifyOTPView, LoginView)


urlpatterns = [
    path("register/request-otp/",RegisterRequestOTPView.as_view(),),
    path("register/verify-otp/",RegisterVerifyOTPView.as_view(),),
    path("login/", LoginView.as_view(),),
    path("logout/",LogoutView.as_view(),),
]