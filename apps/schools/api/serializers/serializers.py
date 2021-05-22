from rest_framework import serializers
from apps.schools.models import School


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'

