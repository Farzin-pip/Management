from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('building/', include('buildings.urls', namespace='buildings')),
    path('expense/', include('expenses.urls', namespace='expenses')),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
]