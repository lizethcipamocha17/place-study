# PyJWT
import jwt
# Django
from django.conf import settings
from django.contrib.auth import password_validation
from django.utils import timezone
# Django REST Framework
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

ACCOUNT_ACTIVATION_TOKEN_TYPE = 'account_activation'
RESET_PASSWORD_TOKEN_TYPE = 'reset_password'
CHANGE_EMAIL_CONFIRMATION = 'change_email_confirmation'


def verify_token(token, token_type=None):
    """This function validates the token type and its expiration date"""

    try:
        payload = jwt.decode(token, settings.SECRET_KEY_TOKEN, algorithms="HS256")
    except jwt.ExpiredSignatureError:
        raise serializers.ValidationError('Este enlace ha caducado')
    except jwt.PyJWTError:
        raise serializers.ValidationError('El enlace es invalido')

    if token_type is not None:
        if payload['data']['type'] != token_type:
            raise serializers.ValidationError('El enlace es invalido')
    return payload


def create_token_jwt(sub, expiration_date, data):
    """This function returns a JWT token"""

    encoded_jwt = jwt.encode({
        'exp': timezone.now() + expiration_date,
        'iat': timezone.now(),
        'sub': sub,
        'data': data,
    }, settings.SECRET_KEY_TOKEN, algorithm='HS256')
    return encoded_jwt


def validate_password(data, instance):
    """This function returns the validation of a password"""

    if data['password'] != data['password_confirm']:
        raise serializers.ValidationError(
            {'password_confirm': "Los campos de la contraseña nueva no coinciden."})
    try:
        password_validation.validate_password(data['password'], instance)
    except ValidationError as error:
        raise serializers.ValidationError(
            {'password_confirm': error.messages}, code='password_confirm')
    return data
