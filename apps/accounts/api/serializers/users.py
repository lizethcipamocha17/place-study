# Django REST framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token

# Models
from apps.accounts.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'contact_email', 'birthday_date', 'photo', 'username', 'school_id'
        )

        read_only_fields = ('first_name', 'school_id')


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            'password', 'last_login', 'is_superuser', 'type_user', 'is_active', 'is_staff', 'date_creation', 'groups',
            'user_permissions'
        )
