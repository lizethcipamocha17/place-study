# Django REST framework
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Models
from apps.accounts.models import User

# Serializers
from apps.accounts.api.serializers.users import (
    UserStudentListSerializer,
    UserTeacherSerializer,
    ChangePasswordSerializer,
    UserAdminSerializer,
    UpdateAvatarSerializer,
    UserInvitedSerializer, UserCreateSerializer, UserListSerializer, UserUpdateSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserStudentListSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        if self.request.user.type_user == User.Type.TEACHER:
            queryset = queryset.filter(teacher=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        if request.user.type_user == User.Type.ADMIN:
            serializer = UserCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user_created = serializer.save()
            return Response(UserListSerializer(user_created).data, status=status.HTTP_201_CREATED)
        raise PermissionDenied(detail="No tienes permiso para realizar esta acción")

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = UserListSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def update(self, request, *args, **kwargs):
        if request.user.type_user != User.Type.ADMIN:
            raise PermissionDenied(detail="No tienes permiso para realizar esta acción")
        user = self.get_object()
        partial = request.method == 'PATCH'
        serializer = UserUpdateSerializer(user, data=request.data, partial=partial, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        if request.user.type_user != User.Type.ADMIN:
            raise PermissionDenied(detail="No tienes permiso para realizar esta acción")
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({'message': 'El usuario fue eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get', 'put', 'patch'])
    def profile(self, request):
        """Service for user profile"""

        user = request.user

        if request.method == 'GET':
            if user.type_user == User.Type.STUDENT:
                user_serializer = self.get_serializer(user)
            elif user.type_user == User.Type.TEACHER:
                user_serializer = UserTeacherSerializer(user)
            elif user.type_user == User.Type.ADMIN:
                user_serializer = UserAdminSerializer(user)
            else:
                user_serializer = UserInvitedSerializer(user)
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        else:
            """Service for update user profile"""
            partial = request.method == 'PATCH'

            if user.type_user == User.Type.STUDENT:
                user_serializer = self.get_serializer(user, data=request.data, partial=partial)
            elif user.type_user == User.Type.TEACHER:
                user_serializer = UserTeacherSerializer(user, data=request.data, partial=partial)
            elif user.type_user == User.Type.ADMIN:
                user_serializer = UserAdminSerializer(user, data=request.data, partial=partial)
            else:
                user_serializer = UserInvitedSerializer(user, data=request.data, partial=partial)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)

        # def change email  ---------- no eliminar

    @action(detail=False, methods=['put'])
    def avatar(self, request):
        """Service for save url of avatar"""
        serializer = UpdateAvatarSerializer(request.user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Avatar actualizado correctamente'}, status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='change-password')
    def change_password(self, request):
        """Service for update user's password"""
        serializer = ChangePasswordSerializer(request.user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Contraseña actualizada correctamente'}, status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
