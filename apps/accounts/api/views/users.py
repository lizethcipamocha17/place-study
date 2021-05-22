# Django REST framework


from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Models
from apps.accounts.models import User

# Serializers
from apps.accounts.api.serializers.users import UserProfileSerializer, TeacherSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_active=True)
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer

    @action(detail=False, methods=['get'])
    def user_profile(self, request):
        """User profile"""
        user_serializer = UserProfileSerializer(request.user)

        return Response(user_serializer.data)

    @action(detail=False, methods=['put'])
    def update_user_profile(self, request, *args, **kwargs):
        """update user"""
        user_serializer = self.serializer_class(request.user, data=request.data, partial=True)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        return Response(user_serializer.data, status=status.HTTP_200_OK)


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(type_user='TCHR')
    serializerClass = TeacherSerializer

    @action(detail=False, methods=['get'])
    def teacher_list(self, request):
        teacher_serializer = TeacherSerializer(request.user)
        return Response(teacher_serializer.data)
