# Django REST framework
from django.contrib.auth import password_validation
# Django
from django.core.exceptions import ValidationError
from rest_framework import serializers

# Models
from apps.accounts.models import User
from apps.schools.api.serializers.serializers import SchoolSerializer

from apps.utils.accounts import validate_password


class UserCreateSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(min_length=8)

    class Meta:
        model = User
        exclude = (
            'is_superuser', 'is_staff', 'last_login', 'created_at', 'updated_at', 'groups', 'user_permissions', 'terms'
        )

    def validate(self, data):
        """Verify passwords match"""
        return validate_password(data, self.instance)

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.terms = True
        if self.validated_data['type_user'] == User.Type.STUDENT:
            user.is_superuser = False
        elif self.validated_data['type_user'] == User.Type.TEACHER:
            user.is_staff = True
            user.is_superuser = False
        else:
            user.is_superuser = True
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'last_login', 'created_at', 'updated_at', 'groups', 'user_permissions')


class UserAdminSerializer(serializers.ModelSerializer):
    """
    UserAdminSerializer is the serializer for type user Admin
    """
    school = SchoolSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'birthday_date', 'photo', 'username', 'school',
                  'type_user', 'is_staff', 'is_active', 'is_superuser')


class UserTeacherSerializer(serializers.ModelSerializer):
    """
    UserTeacherSerializer is the serializer for type user teacher
    """
    school = SchoolSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'birthday_date', 'photo', 'username', 'school', 'type_user'
        )


class UserTeacherListRelatedSerializer(serializers.ModelSerializer):
    """
    User teacher list related serializers
    Must be used for relational fields with read only
    """

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'photo', 'username'
        )
        read_only_fields = ('email',)


class UserListSerializer(serializers.ModelSerializer):
    teacher = UserTeacherListRelatedSerializer(read_only=True)

    class Meta:
        model = User
        exclude = ('password', 'groups', 'user_permissions')


class UserStudentListSerializer(serializers.ModelSerializer):
    """
    UserStudentSerializer is the serializer for type user students
    """

    school = SchoolSerializer(read_only=True)
    teacher = UserTeacherListRelatedSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'teacher', 'birthday_date', 'photo', 'username', 'school',
            'type_user', 'terms'
        )
        read_only_fields = ('first_name', 'last_name', 'email', 'birthday_date', 'photo')


class UserInvitedSerializer(serializers.ModelSerializer):
    """
    UserGenericInSerializer is the serializer for type user generic
    """

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'birthday_date', 'photo', 'username', 'type_user'
        )


class ChangePasswordSerializer(serializers.Serializer):
    """
    ChangePasswordSerializer is the Serializer for password change endpoint.
    """

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_confirmation = serializers.CharField(required=True)

    def validate_old_password(self, value):
        """This function returns the validate old password field"""
        if not self.instance.check_password(value):
            raise serializers.ValidationError(
                'Su contraseña actual es incorrecta.Por favor ingresala de nuevo.'
            )
        return value

    def validate(self, data):
        """This function returns the validated new password field"""

        if data['new_password'] != data['new_password_confirmation']:
            raise serializers.ValidationError(
                {'new_password_confirmation': "Los campos de la contraseña nueva no coinciden."})
        try:
            password_validation.validate_password(data['new_password'], self.instance)
        except ValidationError as error:
            raise serializers.ValidationError(
                {'new_password_confirmation': error.messages}, code='new_password_confirmation'
            )
        return data

    def update(self, instance, validated_data):
        """This function update new password field """
        self.instance.set_password(validated_data['new_password_confirmation'])
        self.instance.save(update_fields=['password', 'updated_at'])
        return self.instance


class UpdateAvatarSerializer(serializers.Serializer):
    """
    UpdateAvatarSerializer is the serializer to update the user's avatar
    """
    photo = serializers.CharField(required=True)

    def update(self, instance, validated_data):
        """This function is used for update the user's avatar"""
        instance.photo = validated_data['photo']
        instance.save(update_fields=['photo', 'updated_at'])
        return instance
