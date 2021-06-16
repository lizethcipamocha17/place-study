import jwt
from django.conf import settings
from django.contrib.auth import password_validation
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


def verify_token(token, token_type=None):
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


def send_email(subject, from_email, to, template, context):
    content = render_to_string(template, context)
    msg = EmailMultiAlternatives(subject, content, from_email, [to])
    msg.attach_alternative(content, "text/html")
    return msg.send()


def get_site_domain(request):
    current_site = get_current_site(request).domain
    return f'{request.scheme}://{current_site}'


def create_token_jwt(sub, expiration_date, data):
    encoded_jwt = jwt.encode({
        'exp': timezone.now() + expiration_date,
        'iat': timezone.now(),
        'sub': sub,
        'data': data,
    }, settings.SECRET_KEY_TOKEN, algorithm='HS256')
    return encoded_jwt


def validate_password(data, instance):
    if data['password'] != data['password_confirm']:
        raise serializers.ValidationError(
            {'password_confirm': "Los campos de la contraseña nueva no coinciden."})
    try:
        password_validation.validate_password(data['password'], instance)
    except ValidationError as error:
        raise serializers.ValidationError(
            {'password_confirm': error.messages}, code='password_confirm')
    return data
