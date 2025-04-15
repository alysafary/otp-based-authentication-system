from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from users.utils import PHONE_REGEX_PATTERN


class User(AbstractUser):
    username = None
    phone_number = models.CharField(
        max_length=16,
        unique=True,
        validators=[RegexValidator(regex=PHONE_REGEX_PATTERN, message='Invalid Phone Number')],
    )

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone_number
