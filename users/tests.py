from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from users.models import User

User = get_user_model()


class AuthenticationTests(TestCase):
    def setUp(self):
        self.valid_phone = '09121234567'
        self.valid_password = 'StrongPass123!'
        self.valid_otp = '123456'
        self.user = User.objects.create(phone_number=self.valid_phone)
        self.user.set_password(self.valid_password)
        self.user.save()

    # LoginRequestView Tests
    def test_login_request_valid_phone(self):
        response = self.client.post(reverse("login_request"), {'phone_number': self.valid_phone})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('detail', response.data)

    def test_login_request_invalid_phone_format(self):
        response = self.client.post(reverse("login_request"), {'phone_number': 'invalid'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('users.otp_service.OTPService.send_otp')
    def test_login_request_new_user_sends_otp(self, mock_send_otp):
        mock_send_otp.return_value = (True, '123456')
        new_phone = '09876543210'
        response = self.client.post(reverse("login_request"), {'phone_number': new_phone})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_send_otp.assert_called_once_with(new_phone)

    # PasswordAuthenticationView Tests
    def test_password_auth_valid_credentials(self):
        cache.clear()
        response = self.client.post(reverse("password_authenticate"), {
            'phone_number': self.valid_phone,
            'password': self.valid_password
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_password_auth_invalid_credentials(self):
        cache.clear()
        response = self.client.post(reverse("password_authenticate"), {
            'phone_number': self.valid_phone,
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_password_auth_blocked_after_multiple_attempts(self):
        for _ in range(5):
            self.client.post(reverse("password_authenticate"), {
                'phone_number': self.valid_phone,
                'password': 'wrongpassword'
            })
        response = self.client.post(reverse("password_authenticate"), {
            'phone_number': self.valid_phone,
            'password': self.valid_password
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # OTPVerifyView Tests
    @patch('users.otp_service.OTPService.validate_otp')
    def test_otp_verify_valid_code(self, mock_validate_otp):
        mock_validate_otp.return_value = True
        phone_number = "09111401444"
        response = self.client.post(reverse("otp_verify"), {
            'phone_number': phone_number,
            'code': self.valid_otp
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(User.objects.filter(phone_number=phone_number).exists())

    @patch('users.otp_service.OTPService.validate_otp')
    def test_otp_verify_invalid_code(self, mock_validate_otp):
        mock_validate_otp.return_value = False
        response = self.client.post(reverse("otp_verify"), {
            'phone_number': self.valid_phone,
            'code': 'wrongcode'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # SignupCompleteView Tests
    def test_signup_complete_valid_data(self):
        user = User.objects.create(phone_number='09967654321')
        response = self.client.post(reverse("signup_complete"), {
            'phone_number': '09967654321',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password': 'NewPass123!'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'John')

    def test_signup_complete_invalid_password(self):
        response = self.client.post(reverse("signup_complete"), {
            'phone_number': self.valid_phone,
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password': 'weak'  # Too short
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Edge Cases
    def test_nonexistent_user_password_auth(self):
        response = self.client.post(reverse("password_authenticate"), {
            'phone_number': '09000000000',
            'password': 'anypassword'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
