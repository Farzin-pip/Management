import hashlib
from rest_framework.throttling import AnonRateThrottle, SimpleRateThrottle


class OtpPhoneRateThrottle(SimpleRateThrottle):
    scope = 'otp_phone'

    def get_cache_key(self, request, view) -> str | None:
        phone_number = request.data.get('phone_number')

        if not phone_number:
            return None

        phone_hash = hashlib.sha256(
            str(phone_number).encode()
        ).hexdigest()

        return self.cache_format % {
            'scope': self.scope,
            'ident': phone_hash
        }
