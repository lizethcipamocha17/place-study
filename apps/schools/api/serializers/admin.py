# Django Rest Framework
from rest_framework import serializers
# Models
from apps.accounts.models import User
from apps.utils.accounts import validate_password


class UserCreateSerializer(serializers.ModelSerializer):
    """
    UserStudentSerializer is serializer for created type user student in administration
    """

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'birthday_date', 'username', 'email',
                  'password', 'school', 'teacher', 'password_confirm')

    def validate(self, data):
        """This function returns the validated password field"""
        return validate_password(data, self.instance)
