# Django REST framework
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# From models
from apps.accounts.models import User

# Serializers
from apps.accounts.api.serializers.users import UserStudentSerializer, UserTeacherSerializer, ChangePasswordSerializer, \
    UserAdminSerializer, UpdateAvatarSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_active=True)
    permission_classes = (IsAuthenticated,)
    serializer_class = UserStudentSerializer

    @action(detail=False, methods=['get', 'put', 'patch'])
    def profile(self, request):
        """User profile"""

        user = request.user
        user_serializer = None

        if request.method == 'GET':
            if user.type_user == User.Type.STUDENT:
                user_serializer = self.get_serializer(user)
            elif user.type_user == User.Type.TEACHER:
                user_serializer = UserTeacherSerializer(user)
            elif user.type_user == User.Type.ADMIN:
                user_serializer = UserAdminSerializer(user)
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        else:
            """update user"""
            partial = request.method == 'PATCH'

            if user.type_user == User.Type.STUDENT:
                user_serializer = self.get_serializer(user, data=request.data, partial=partial)
            elif user.type_user == User.Type.TEACHER:
                user_serializer = UserTeacherSerializer(user, data=request.data, partial=partial)
                print("REQUEST DATA", request.data)
            elif user.type_user == User.Type.ADMIN:
                user_serializer = UserAdminSerializer(user, data=request.data, partial=partial)

            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['put'])
    def avatar(self, request):
        serializer = UpdateAvatarSerializer(request.user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Avatar actualizado correctamente'}, status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='change-password')
    def change_password(self, request):
        """Update password"""
        serializer = ChangePasswordSerializer(request.user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Contraseña actualizada correctamente'}, status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

