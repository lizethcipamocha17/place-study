# Django
from django.contrib.auth import password_validation, authenticate

# Django REST framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

# Models
from apps.accounts.models import User


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'birthday_date', 'school_id', 'username', 'email']


class UserLoginSerializer(serializers.Serializer):
    # Campos que vamos a requerir
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=30)

    # Primero validamos los datos
    def validate(self, data):
        # authenticate recibe las credenciales, si son válidas devuelve el objeto del usuario
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Los datos de usuario no son válidos')

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
    User create serializer
    """
    password_confirmation = serializers.CharField(min_length=8, max_length=30)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'birthday_date',
                  'school_id', 'user_id', 'username', 'email', 'password', 'password_confirmation']

    def validate(self, data):
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        password_validation.validate_password(passwd)

    def create(self, data):
        data.pop('password_confirmation')
        user = User.objects.create_user(**data)
        return user
