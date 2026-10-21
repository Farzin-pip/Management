from django.urls import path
from .views import UserView, RegisterView, LoginView, LogoutView, SendOtpView

app_name = 'accounts'
urlpatterns = [
    path('user/', UserView.as_view()),
    path('user/<int:pk>/', UserView.as_view()),
    path("send_otp/", SendOtpView.as_view()),
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
]