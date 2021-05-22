from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.schools.models import School
from rest_framework.decorators import action
from apps.schools.api.serializers.serializers import SchoolSerializer
from rest_framework import viewsets


# Create your views here.
class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer


@action(detail=False, methods=['get'])
def school_list(request):
    """
    List all code Schools
    """
    school_serializer = SchoolSerializer(request.school)
    return Response(school_serializer.data)
