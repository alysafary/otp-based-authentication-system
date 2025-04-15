from django.contrib.auth import get_user_model, authenticate
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.otp_service import OTPService
from users.serializers import PhoneNumberSerializer, LoginSerializer, OTPVerifySerializer, RegisterCompleteSerializer
from users.throttles import LoginAttemptTracker

User = get_user_model()


class BaseAuthenticationView(APIView):
    """
    A base view class providing common authentication utilities.

    Includes methods for checking whether a user or IP is blocked due to repeated
    failed attempts, handling failed attempts by updating the attempt counters,
    and resetting those counters on successful authentication.
    """

    def check_blocked(self, phone, ip):
        ip_tracker = LoginAttemptTracker(f"ip:{ip}")
        phone_tracker = LoginAttemptTracker(f"phone:{phone}")

        if ip_tracker.is_blocked() or phone_tracker.is_blocked():
            return True, ip_tracker, phone_tracker

        return False, ip_tracker, phone_tracker

    def handle_failed_attempts(self, ip_tracker, phone_tracker):
        ip_tracker.register_failed_attempt()
        phone_tracker.register_failed_attempt()

    def reset_attempts(self, ip_tracker, phone_tracker):
        ip_tracker.reset_attempts()
        phone_tracker.reset_attempts()


class LoginRequestView(APIView):
    """
    Handles the initial login request using a phone number.

    If the phone number is already associated with a registered user, prompts for a password.
    Otherwise, sends a one-time verification code (OTP) to the phone number for registration.
    """

    def post(self, request):
        serializer = PhoneNumberSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"detail": "Invalid phone number format."},
                status=status.HTTP_400_BAD_REQUEST
            )

        phone_number = serializer.validated_data['phone_number']

        if User.objects.filter(phone_number=phone_number).exists():
            return Response(
                {"detail": "Please enter your password to continue.", "phone_number": phone_number},
            )

        success, otp = OTPService.send_otp(phone_number)

        if success:
            return Response(
                {"detail": "A one-time verification code has been sent to your phone number."}
            )

        return Response(
            {"detail": "Failed to send verification code. Please try again later."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class PasswordAuthenticationView(BaseAuthenticationView):
    """
    Authenticates users via phone number and password.

    Checks if the IP address or phone number is blocked due to failed attempts.
    On success, resets attempt counters; on failure, increments them accordingly.
    """

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone_number']
            ip = request.META.get("REMOTE_ADDR")

            is_blocked, ip_tracker, phone_tracker = self.check_blocked(phone, ip)
            if is_blocked:
                return Response({"detail": "Your account or IP has been temporarily blocked."}, status=403)

            user = authenticate(phone_number=phone, password=serializer.validated_data['password'])
            if user:
                self.reset_attempts(ip_tracker, phone_tracker)
                return Response({"detail": "Login successful."})

            self.handle_failed_attempts(ip_tracker, phone_tracker)
            return Response({"detail": "Incorrect username or password."}, status=401)

        return Response(serializer.errors, status=400)


class OTPVerifyView(BaseAuthenticationView):
    """
    Verifies the OTP code submitted by the user.

    Validates that the IP or phone number is not blocked. If the OTP is valid,
    resets the failed attempt counters and ensures a user account exists for the phone number.
    """

    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        phone = serializer.validated_data['phone_number']
        code = serializer.validated_data['code']
        ip = request.META.get("REMOTE_ADDR")

        is_blocked, ip_tracker, phone_tracker = self.check_blocked(phone, ip)
        if is_blocked:
            return Response(
                {"detail": "Your access has been temporarily blocked due to multiple failed attempts."},
                status=status.HTTP_403_FORBIDDEN
            )

        if OTPService.validate_otp(phone, code):
            self.reset_attempts(ip_tracker, phone_tracker)
            User.objects.get_or_create(phone_number=phone)

            return Response(
                {"detail": "Verification successful. Proceed to complete your registration.", "phone_number": phone})

        self.handle_failed_attempts(ip_tracker, phone_tracker)

        return Response(
            {"detail": "Invalid or expired verification code."},
            status=status.HTTP_400_BAD_REQUEST
        )


class SignupCompleteView(APIView):
    """
    Completes the signup process after OTP verification.

    Updates the user instance with the additional registration data and marks
    the registration process as complete within a transaction.
    """

    @transaction.atomic
    def post(self, request):
        serializer = RegisterCompleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']
        user = User.objects.get(phone_number=phone_number)

        serializer.update(user, serializer.validated_data)

        return Response({
            "detail": "Registration completed successfully.",
            "data": {
                "phone_number": str(user.phone_number)
            }
        }, status=status.HTTP_200_OK)
