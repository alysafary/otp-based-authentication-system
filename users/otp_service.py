from django.core.cache import cache
from django.utils.crypto import get_random_string


class OTPService:
    """
    A utility class for managing One-Time Password (OTP) operations.

    This service provides methods to generate, send, and validate OTPs
    using a caching system. It is typically used for phone number
    verification or similar authentication flows.
    """

    @staticmethod
    def _get_cache_key(phone_number):
        return f"otp:{phone_number}"

    @staticmethod
    def _generate_otp():
        return get_random_string(length=6, allowed_chars='0123456789')

    @staticmethod
    def send_otp(phone_number):
        otp = OTPService._generate_otp()
        cache_key = OTPService._get_cache_key(phone_number)
        cache.set(cache_key, otp, timeout=30)
        print("OTP sent successfully:  {}".format(otp))
        return True, otp

    @staticmethod
    def validate_otp(phone_number, otp):
        cache_key = OTPService._get_cache_key(phone_number)
        cached_otp = cache.get(cache_key)
        return cached_otp == otp
