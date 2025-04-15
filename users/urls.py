from django.urls import path

from users.views import LoginRequestView, PasswordAuthenticationView, OTPVerifyView, SignupCompleteView

urlpatterns = [
    path("login/request/", LoginRequestView.as_view(), name='login_request'),
    path("login/password/", PasswordAuthenticationView.as_view(), name='password_authenticate'),
    path("login/verify/", OTPVerifyView.as_view(), name='otp_verify'),
    path("signup/complete/", SignupCompleteView.as_view(), name='signup_complete'),
]
