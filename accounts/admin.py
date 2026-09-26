from django.contrib import admin
from .models import User, OtpCode


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'phone_number',
        'first_name',
        'last_name',
        'is_active',
        'is_staff',
        'created_at',
    )
    list_filter = ('is_active', 'is_staff')
    search_fields = ('phone_number', 'first_name', 'last_name')


@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = (
        'phone_number',
        'code',
        'created',
    )
    search_fields = ('phone_number',)