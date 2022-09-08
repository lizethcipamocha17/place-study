# Django Rest Framework
from rest_framework import serializers

# Models
from apps.schools.models import School


class SchoolSerializer(serializers.ModelSerializer):
    """
    SchoolSerializer is serializer of school
    """

    class Meta:
        model = School
        fields = '__all__'
