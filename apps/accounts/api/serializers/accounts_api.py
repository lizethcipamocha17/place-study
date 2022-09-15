# Django
from django.conf import settings
from django.contrib.auth import authenticate
# Rest Framework
from django.utils import timezone
from rest_framework import serializers
from rest_framework.authtoken.models import Token

# Models
from rest_framework.exceptions import PermissionDenied

from apps.accounts.models import User
# Utils
from apps.utils.accounts import (
    verify_token,
    create_token_jwt,
    validate_password,
    CHANGE_EMAIL_CONFIRMATION,
    RESET_PASSWORD_TOKEN_TYPE,
    ACCOUNT_ACTIVATION_TOKEN_TYPE
)
from apps.utils.utils import send_email, get_site_domain


class UserModelSerializer(serializers.ModelSerializer):
    """
    UserModelSerializer is used to display information after the user login
    """

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'birthday_date', 'school_id', 'username', 'email']


class UserLoginSerializer(serializers.Serializer):
    """
    UserLoginSerializer is serializer of Login
    """

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=30)

    def validate(self, data):
        """Authenticate receives the credentials, if they are valid it returns the user's object"""
        user = authenticate(email=data['email'], password=data['password'])

        if not user:
            raise serializers.ValidationError('Email o contraseña incorrectos')

        if not user.is_active:
            raise serializers.ValidationError('Su cuenta esta inactiva')
        else:
            """save the user in the context for later in create to retrieve the token"""
            self.context['user'] = user
            return data

    def create(self, data):
        """Generate or retrieve token."""
        user = self.context['user']
        token, created = Token.objects.get_or_create(user=user)
        if not created:
            token.delete()
            token = Token.objects.create(user=user)

        # verificar si inicia sesión por primera vez
        self.context['first_time_login'] = True if user.last_login is None else False
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])

        return self.context['user'], token.key


class UserSignUpSerializer(serializers.ModelSerializer):
    """
    UserSignUpSerializer is serializer of signUp
    """

    password_confirm = serializers.CharField(min_length=8, max_length=30)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'birthday_date', 'username', 'email',
                  'password', 'school', 'teacher', 'password_confirm')

    def validate(self, data):
        """This function returns the validated password field"""
        return validate_password(data, self.instance)

    def save(self, **kwargs):
        """This function saves a user's record and send an email for validation"""
        school = self.validated_data['school'].school_id
        self.validated_data['type_user'] = User.Type.INVITED if school == 1 else User.Type.STUDENT

        self.validated_data.pop('school')
        self.validated_data.pop('password_confirm')

        user = User.objects.create_user(**self.validated_data, school=school)
        token = Token.objects.create(user=user)

        """Send account validation email"""
        self.send_email_account_activation(user)
        return user, token.key

    def send_email_account_activation(self, user):
        """This function returns the body of an email for the validation of a user's account"""
        email = user.teacher.email if user.type_user == User.Type.STUDENT else settings.DEFAULT_ADMIN_EMAIL

        token_jwt = create_token_jwt(
            email,
            settings.JWT_ACTIVATION_ACCOUNT_EXPIRE_DELTA,
            data={
                'full_name': user.full_name,
                'school_name': user.school.school_name,
                'email': user.email,
                'type': ACCOUNT_ACTIVATION_TOKEN_TYPE,
            },
        )
        site = get_site_domain(self.context['request'])
        context = {
            'teacher_first_name': user.teacher.first_name if user.type_user == User.Type.STUDENT else None,
            'user_full_name': user.full_name,
            'user_type': user.type_user if user.type_user == User.Type.STUDENT else User.Type.ADMIN,
            'site': f'{site}/home/accountactivation/{token_jwt}'
        }

        subject = 'Verificación de cuenta de usuario'
        template = 'accounts/emails/account_activation.html'
        send_email(subject, settings.DEFAULT_FROM_EMAIL, email, template, context)


class ResetPasswordSerializer(serializers.Serializer):
    """
      ResetPasswordSerializer is serializer for resert password of the users
      with send email
     """
    email = serializers.EmailField()

    def validate_email(self, data):
        """This function is used to validate that the email entered by the user is stored in the database"""
        user = User.objects.filter(is_active=True, email=data).first()
        if user is None:
            raise serializers.ValidationError({'message': " No hay una cuenta con este email"})
        self.instance = user
        return data

    def save(self, **kwargs):
        """This function is used for save the new password """
        self.send_email_reset_password(self.instance)
        return self.instance

    def send_email_reset_password(self, user):
        """This function send email so that the user can retrieve the password for the account"""
        token_jwt = create_token_jwt(
            user.email,
            settings.JWT_RESET_PASSWORD_EXPIRE_DELTA,
            data={
                'email': user.email,
                'type': RESET_PASSWORD_TOKEN_TYPE,

            },
        )
        url_site = get_site_domain(self.context['request'])
        context = {
            'first_name': user.first_name,
            'site': f'{url_site}/accounts/recovery/password/{token_jwt}'
        }

        subject = 'Recuperar contraseña'
        template = 'accounts/emails/reset_password.html'
        send_email(subject, settings.DEFAULT_FROM_EMAIL, user.email, template, context)


class AccountActivationSerializer(serializers.Serializer):
    """
    AccountActivationSerializer is serializer for account activation
    """
    token = serializers.CharField(max_length=555)

    def validate_token(self, data):
        """ This function is used for validate token"""
        self.context['payload'] = verify_token(data, ACCOUNT_ACTIVATION_TOKEN_TYPE)
        return data

    def save(self, **kwargs):
        """This function is used for save the user's account activation"""
        user = User.objects.get(email=self.context['payload']['data']['email'])
        user.is_active = True
        user.save(update_fields=['is_active', 'updated_at'])

        """Send email user notification """
        self.send_email_account_activation(user)

    def send_email_account_activation(self, user):
        """This function send email notify user that their account has been activated"""
        context = {
            'first_name': user.first_name,
            'teacher_name': user.teacher.full_name if user.type_user == User.Type.STUDENT else None
        }
        subject = 'Validación de ingreso'
        template = 'accounts/emails/notification_user.html'
        send_email(subject, settings.DEFAULT_FROM_EMAIL, user.email, template, context)


class VerifyTokenSerializer(serializers.Serializer):
    """
    VerifyTokenSerializer is serializer for verify token
    """
    token = serializers.CharField(max_length=555)

    def validate_token(self, data):
        """ This function is used for validate token"""
        self.context['payload'] = verify_token(data)
        return data


class PasswordResetFromKeySerializer(serializers.Serializer):
    """
    PasswordResetFromKeySerializer is serializer for reset password.
    """
    token = serializers.CharField(max_length=555)
    password = serializers.CharField()
    password_confirm = serializers.CharField()

    def validate_token(self, data):
        """This function is used for validate token for rest password"""
        self.context['payload'] = verify_token(data, RESET_PASSWORD_TOKEN_TYPE)
        return data

    def validate(self, data):
        """This function returns the validated password field"""
        return validate_password(data, self.instance)

    def save(self, **kwargs):
        """This function is used to save the reset password"""
        user = User.objects.get(email=self.context['payload']['data']['email'], is_active=True)
        user.set_password(self.validated_data['password_confirm'])
        user.save(update_fields=['password', 'updated_at'])
        return user


class ChangeEmail(serializers.Serializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        user = User.objects.filter(email=value).first()
        if user is not None:
            raise serializers.ValidationError('Este correo electrónico ya esta asociado a una cuenta')
        return value

    def save(self, **kwargs):
        """This function is used for save the new password """
        user = self.validated_data['user']
        if user.type_user == user.Type.STUDENT:
            raise PermissionDenied(detail='No tiene permisos para actualizar el correo')

        send = self.send_confirm_email(user, self.validated_data['email'])
        self.context['send_email'] = True if send == 1 else False
        return user

    def send_confirm_email(self, user, email):
        """This function send email so that the user can retrieve the password for the account"""
        token_jwt = create_token_jwt(
            email,
            settings.JWT_CHANGE_EMAIL_CONFIRMATION_EXPIRE_DELTA,
            data={
                'email': email,
                'type': CHANGE_EMAIL_CONFIRMATION,

            },
        )
        url_site = get_site_domain(self.context['request'])
        context = {
            'first_name': user.first_name,
            'site': f'{url_site}/accounts/email/change/{token_jwt}'
        }

        subject = 'Confirmación de cuenta de correo electrónico'
        template = 'accounts/emails/change_email_confirmation.html'
        return send_email(subject, settings.DEFAULT_FROM_EMAIL, email, template, context)


class ConfirmEmailSerializer(serializers.Serializer):
    """
    PasswordResetFromKeySerializer is serializer for reset password.
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    token = serializers.CharField(max_length=555)

    def validate_token(self, data):
        """This function is used for validate token for rest password"""
        self.context['payload'] = verify_token(data, CHANGE_EMAIL_CONFIRMATION)
        return data

    def save(self, **kwargs):
        """This function is used to save the reset password"""
        user = self.validated_data['user']
        user.email = self.context['payload']['data']['email']
        user.save(update_fields=['email', 'updated_at'])
        return user
