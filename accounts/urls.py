from django.urls import path
from .views import UserView


app_name = 'accounts'
urlpatterns = [
    path('user/', UserView.as_view()),
    path('user/<int:pk>/', UserView.as_view()),
]