from django.core.cache import cache
from django.utils import timezone


class LoginAttemptTracker:
    """
    Tracks failed login attempts and temporarily blocks further attempts after a limit is reached.

    This class uses a caching backend to store the number of failed attempts associated with
    a unique key (such as a phone number or IP address). If the number of failed attempts exceeds
    a defined threshold (`MAX_ATTEMPTS`), the user is considered blocked for a specified duration
    (`BLOCK_DURATION`).
    """

    MAX_ATTEMPTS = 3
    BLOCK_DURATION = 60 * 60

    def __init__(self, key_prefix):
        self.key_prefix = key_prefix

    def _key(self):
        return f"login_fail:{self.key_prefix}"

    def is_blocked(self):
        data = cache.get(self._key())
        if not data:
            return False
        attempts, timestamp = data
        return attempts >= self.MAX_ATTEMPTS

    def register_failed_attempt(self):
        now = timezone.now()
        data = cache.get(self._key())

        if not data:
            cache.set(self._key(), (1, now), timeout=self.BLOCK_DURATION)
        else:
            attempts, timestamp = data
            attempts += 1
            cache.set(self._key(), (attempts, timestamp), timeout=self.BLOCK_DURATION)

    def reset_attempts(self):
        cache.delete(self._key())
