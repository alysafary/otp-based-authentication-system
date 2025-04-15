from users.throttles import LoginAttemptTracker

PHONE_REGEX_PATTERN = "^(0)(9[0-9]{9})$"


def blocked_access(ip, phone_number):
    """
    Checks whether access should be blocked based on failed login attempts
    from either the IP address or the phone number.

    Args:
        ip (str): The IP address of the client.
        phone_number (str): The phone number being used for login.

    Returns:
        bool: True if either the IP or phone number has exceeded the allowed
              number of failed login attempts and is currently blocked;
              otherwise, False.
    """

    ip_tracker = LoginAttemptTracker(f"ip:{ip}")
    phone_tracker = LoginAttemptTracker(f"phone:{phone_number}")
    return ip_tracker.is_blocked() or phone_tracker.is_blocked()
