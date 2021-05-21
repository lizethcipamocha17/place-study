# Django REST framework
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Models
from apps.accounts.models import User

# Serializers
from apps.accounts.api.serializers.users import UserProfileSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserProfileSerializer

    @action(detail=False, methods=['get'])
    def user_profile(self, request):
        """User profile"""
        user_serializer = UserProfileSerializer(request.user)
        return Response(user_serializer.data)
