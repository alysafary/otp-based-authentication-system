import re

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

User = get_user_model()


class PhoneNumberField(serializers.CharField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.validators.append(self.validate_phone_format)

    def validate_phone_format(self, value):
        cleaned_number = re.sub(r'[^0-9]', '', value)
        if not re.fullmatch(r'^(0)(9[0-9]{9})$', cleaned_number):
            raise serializers.ValidationError(
                "Phone number must be 11 digits starting with 09"
            )
        return cleaned_number

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        return re.sub(r'[^0-9]', '', data)


class PhoneNumberSerializer(serializers.Serializer):
    phone_number = PhoneNumberField()


class LoginSerializer(serializers.Serializer):
    phone_number = PhoneNumberField()
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        trim_whitespace=False
    )


class OTPVerifySerializer(serializers.Serializer):
    phone_number = PhoneNumberField()
    code = serializers.CharField(min_length=6, max_length=6)


class RegisterCompleteSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField()
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        trim_whitespace=False,
        required=True
    )

    class Meta:
        model = User
        fields = ['phone_number', 'password', 'first_name', 'last_name', 'email']
        extra_kwargs = {
            'first_name': {'required': False, 'allow_blank': True, 'default': ''},
            'last_name': {'required': False, 'allow_blank': True, 'default': ''},
            'email': {'required': False, 'allow_blank': True, 'default': ''},
        }

    def validate_phone_number(self, value):
        if not User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("User with this phone number not found.")
        return value

    def validate_password(self, value):
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value

    def validate(self, data):
        if data.get('email'):
            if User.objects.filter(email=data['email']).exclude(phone_number=data['phone_number']).exists():
                raise serializers.ValidationError(
                    {'email': 'This email is already in use by another account.'}
                )
        return data

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.set_password(validated_data['password'])

        instance.save()
        return instance