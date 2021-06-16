# Django
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from rest_framework import serializers
from rest_framework.authtoken.models import Token

# Models
from apps.accounts.models import User
# Utils
from apps.accounts.utils import verify_token, send_email, get_site_domain, create_token_jwt, validate_password

ACCOUNT_ACTIVATION_TOKEN_TYPE = 'account_activation'
RESET_PASSWORD_TOKEN_TYPE = 'reset_password'


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'birthday_date', 'school_id', 'username', 'email']


class UserLoginSerializer(serializers.Serializer):
    """
    UserLoginSerializer is serializer of Login
    """
    # Campos que vamos a requerir
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=30)

    # Primero validamos los datos
    def validate(self, data):
        # authenticate recibe las credenciales, si son válidas devuelve el objeto del usuario

        user = authenticate(email=data['email'], password=data['password'])

        if not user:
            raise serializers.ValidationError('Email o contraseña incorrectos')

        if not user.is_active:
            raise serializers.ValidationError('Su cuenta esta inactiva')
        else:
            # Guardamos el usuario en el contexto para posteriormente en create recuperar el token
            self.context['user'] = user
            return data

    def create(self, data):
        """Generar o recuperar token."""
        token, created = Token.objects.get_or_create(user=self.context['user'])
        # si no fue creado un token, se borra el que existe en la bd y se crea uno nuevo.
        # Para el mismo usuario
        if not created:
            token.delete()
            token = Token.objects.create(user=self.context['user'])
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
        return validate_password(data, self.instance)

    def save(self, **kwargs):
        school = self.validated_data['school'].school_id
        self.validated_data['type_user'] = User.Type.INVITED if school == 1 else User.Type.STUDENT

        self.validated_data.pop('school')
        self.validated_data.pop('password_confirm')

        user = User.objects.create_user(**self.validated_data, school=school)
        token = Token.objects.create(user=user)

        # Enviar correo de validación de cuenta
        self.send_email_account_activation(user)
        return user, token.key

    def send_email_account_activation(self, user):
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
            'site': f'{site}/accounts/students/verify/{token_jwt}'
        }

        subject = 'Verificación de cuenta de estudiante'
        template = 'accounts/emails/account_activation.html'
        send_email(subject, settings.DEFAULT_FROM_EMAIL, email, template, context)


class ResetPasswordSerializer(serializers.Serializer):
    """
      ResetPasswordSerializer is serializer for resert password of the users
      with send email
     """
    email = serializers.EmailField()

    def validate_email(self, data):
        user = User.objects.filter(is_active=True, email=data).first()
        if user is None:
            raise serializers.ValidationError({'message': " No hay una cuenta con este email"})
        self.instance = user
        return data

    def save(self, **kwargs):
        self.send_email_reset_password(self.instance)
        return self.instance

    def send_email_reset_password(self, user):
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
    token = serializers.CharField(max_length=555)

    def validate_token(self, data):
        self.context['payload'] = verify_token(data, ACCOUNT_ACTIVATION_TOKEN_TYPE)
        return data

    def save(self, **kwargs):
        user = User.objects.get(email=self.context['payload']['data']['email'])
        user.is_active = True
        user.save(update_fields=['is_active', 'updated_at'])
        # desde aqui se le envia la notificación al estudiante
        self.send_email_account_activation(user)

    def send_email_account_activation(self, user):
        """
        This function send email notify user that their
        account has been activated
        """
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
        # cambiar tipo validar cualquier tipo de token
        self.context['payload'] = verify_token(data)
        return data


class PasswordResetFromKeySerializer(serializers.Serializer):
    token = serializers.CharField(max_length=555)
    password = serializers.CharField()
    password_confirm = serializers.CharField()

    def validate_token(self, data):
        self.context['payload'] = verify_token(data, RESET_PASSWORD_TOKEN_TYPE)
        return data

    def validate(self, data):
        return validate_password(data, self.instance)

    def save(self, **kwargs):
        user = User.objects.get(email=self.context['payload']['data']['email'], is_active=True)
        user.set_password(self.validated_data['password_confirm'])
        user.save(update_fields=['password', 'updated_at'])
        return user
