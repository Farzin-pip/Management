from django.contrib import admin
from utils.utils import ReadOnlyModelAdmin
from .models import User, OtpCode


@admin.register(User)
class UserAdmin(ReadOnlyModelAdmin):
    list_display = ['id', 'phone_number', 'first_name', 'last_name', 'role', 'is_active', 'created_at']
    list_filter = ['role', 'is_active', 'is_staff']
    search_fields = ['phone_number', 'first_name', 'last_name']
    editable_fields = ['first_name', 'last_name']


@admin.register(OtpCode)
class OtpCodeAdmin(ReadOnlyModelAdmin):
    list_display = ['id', 'phone_number', 'code', 'created_at']
    search_fields = ['phone_number']