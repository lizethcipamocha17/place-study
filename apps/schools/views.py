from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.schools.models import School
from apps.schools.serializers import SchoolSerializer


# Create your views here.

@api_view(['GET'])
def school_list(request):
    """
    List all code Schools
    """
    if request.method == 'GET':
        school = School.objects.all()
        serializer = SchoolSerializer(school, many=True)
        return Response(serializer.data)

