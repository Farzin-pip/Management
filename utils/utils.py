from kavenegar import APIException, KavenegarAPI, HTTPException
from django.conf import settings
from django.utils import timezone
from accounts.models import OtpCode
from accounts.services import generate_otp_code
from django.contrib import admin



def send_otp_code(phone_number: str, code: int):
    try:
        api = KavenegarAPI(settings.KAVENEGAR_API_KEY)

        params = {
            "sender": "2000660110",
            "receptor": phone_number,
            "message": f"Your verification code is: {code}",
        }

        return api.sms_send(params)

    except (APIException, HTTPException) as e:
        print(e)
        return None


def send_otp(phone_number: str) -> bool:
    code = generate_otp_code()
    response = send_otp_code(phone_number, code)

    if response is None:
        return False

    OtpCode.objects.update_or_create(
        phone_number=phone_number,
        defaults={
            "code": code,
            "created_at": timezone.now(),
        },
    )

    return True


class ReadOnlyModelAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        editable_fields = getattr(self, 'editable_fields', [])

        return [
            field.name for field in self.model._meta.fields
            if field.name not in editable_fields
        ]


