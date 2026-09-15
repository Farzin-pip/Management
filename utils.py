import secrets
from django.conf import settings
from django.utils import timezone
from kavenegar import APIException
from kavenegar import HTTPException
from kavenegar import KavenegarAPI
from accounts.models import OtpCode


def generate_otp_code():
    return secrets.randbelow(9000) + 1000


def create_otp(phone_number):
    code = generate_otp_code()

    otp, created = OtpCode.objects.update_or_create(
        phone_number=phone_number,
        defaults={
            "code": code,
            "created": timezone.now(),
        },
    )

    return code


def send_otp_code(phone_number, code):
    try:
        api = KavenegarAPI(settings.KAVENEGAR_API_KEY)

        params = {
            "sender": "2000660110",
            "receptor": phone_number,
            "message": f"Your verification code is: {code}",
        }

        response = api.sms_send(params)

        return response

    except APIException as e:
        print(e)
        return None

    except HTTPException as e:
        print(e)
        return None