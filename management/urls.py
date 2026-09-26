from django.contrib import admin
from django.urls import include, path



urlpatterns = [
    path("admin/", admin.site.urls),
    path('building/', include('buildings.urls', namespace='buildings')),
    path('expense/', include('expenses.urls', namespace='expenses'))
]