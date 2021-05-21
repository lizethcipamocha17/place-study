# Django REST framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token

# Models
from apps.accounts.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['photo', 'first_name', 'last_name', 'username', 'birthday_date', 'email', 'school_id']
