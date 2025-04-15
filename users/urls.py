from django.urls import path

from users.views import LoginRequestView, PasswordAuthenticationView, OTPVerifyView, SignupCompleteView

urlpatterns = [
    path('login/', LoginRequestView.as_view(), name='login_request'),
    path('authenticate/', PasswordAuthenticationView.as_view(), name='password_authenticate'),
    path('verify-otp/', OTPVerifyView.as_view(), name='otp_verify'),
    path('signup-complete/', SignupCompleteView.as_view(), name='signup_complete'),
]
