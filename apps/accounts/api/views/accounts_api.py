# Django REST framework
from datetime import datetime

# Py JWT
# Django
from django.contrib.sessions.models import Session
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.accounts.api.serializers.accounts_api import (
    UserLoginSerializer,
    UserModelSerializer,
    UserSignUpSerializer,
    AccountActivationSerializer, VerifyTokenSerializer, ResetPasswordSerializer, PasswordResetFromKeySerializer,
)
# Serializers
from apps.accounts.api.serializers.users import UserStudentSerializer


class AccountViewSet(viewsets.GenericViewSet):
    # serializer_class = UserSignUpSerializer

    # Detail define si es una petición de detalle o no, en methods añadimos el método permitido,
    # en nuestro caso solo vamos a permitir posts
    @action(detail=False, methods=['post'])
    def login(self, request):
        """User sign in."""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token
        }
        message_login = 'Inicio de sesión exitoso!'
        return Response({'data': data, 'message_login': message_login}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def signup(self, request):
        """User sign up."""
        data = request.data
        serializer = UserSignUpSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        res = {
            'user': UserStudentSerializer(user).data,
            'acess_token': token
        }
        return Response(res, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['Post'], url_path='reset-password-email')
    def reset_password_email(self, request):
        data = request.data
        serializer = ResetPasswordSerializer(data=data, context={'request': request})
        print('SERIALIZER', serializer, data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        res = {
            'email': data,
            'message': 'Email enviado con exito'
        }
        return Response(res, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def logout(self, request, *args, **kwargs):
        try:

            token = request.data.get('token')
            token = Token.objects.filter(key=token).first()

            if token:
                user = token.user
                all_sessions = Session.objects.filter(expire_date__gte=datetime.now())
                if all_sessions.exists():
                    for session in all_sessions:
                        session_data = session.get_decoded()
                        if user.user_id == int(session_data.get('_auth_user_id')):
                            session.delete()

                token.delete()

                session_message = 'Sesiones de usuario eliminadas.'
                token_message = 'Token eliminado.'
                return Response({'token_message': token_message, 'session_message': session_message},
                                status=status.HTTP_200_OK)

            return Response({'error': 'No se ha encontrado un usuario con estas credenciales'},
                            status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error': 'No se ha encontrado token en la petición'}, status=status.HTTP_409_CONFLICT)

    @action(detail=False, methods=['delete'], url_path='delete')
    def delete_account(self, request):
        request.user.is_active = False
        request.user.save()
        return Response({'message': 'Su cuenta se ha eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'], url_path='activation')
    def account_activation(self, request):
        serializer = AccountActivationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'success': True,
            'message': 'Su cuenta ha sido verificada'
        }
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='password-reset-from-key')
    def password_reset_from_key(self, request):
        serializer = PasswordResetFromKeySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'success': True,
            'message': 'Su contraseña ha sido restaurada'
        }
        return Response(data, status=status.HTTP_200_OK)


    @action(detail=False, methods=['post'], url_path='verify-token')
    def verify_token(self, request):
        serializer = VerifyTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = {
            'success': True,
            'payload': serializer.context['payload']
        }
        return Response(data, status=status.HTTP_200_OK)
