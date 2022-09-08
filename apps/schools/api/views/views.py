# Django REST framework
from rest_framework.exceptions import PermissionDenied, ParseError, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, viewsets
# Models
from apps.accounts.models import User
from apps.schools.models import School
# Serializers
from apps.accounts.api.serializers.users import UserTeacherListRelatedSerializer
from apps.schools.api.serializers.serializers import SchoolSerializer
# Utils
from apps.utils.utils import parse_int


# Create your views here.


class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.type_user == User.Type.ADMIN:
            serializer = SchoolSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        raise PermissionDenied(detail="No tienes permiso para realizar esta acción")

    def list(self, request, *args, **kwargs):
        """
        List all Schools
        """
        school_serializer = SchoolSerializer(self.queryset, many=True)
        return Response(school_serializer.data)

    # dudaa-----------------
    def update(self, request, *args, **kwargs):
        if request.user.type_user != User.Type.ADMIN:
            raise PermissionDenied(detail="No tienes permiso para realizar esta acción")
        user = self.get_object()
        partial = request.method == 'PATCH'
        serializer = SchoolSerializer(user, data=request.data, partial=partial, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'Colegio actualizado correctamente', 'data': serializer.data},
                status=status.HTTP_200_OK
            )
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """"""
        if request.user.type_user != User.Type.ADMIN:
            raise PermissionDenied(detail="No tienes permiso para realizar esta acción")
        school = self.get_object()
        school.delete()
        return Response({'message': 'El colegio fue eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)


class TeacherViewSet(viewsets.ModelViewSet):
    """
    TeacherViewSet is view for list all fullname of teachers
    This view is used in the slection box in register
    """
    queryset = User.objects.filter(type_user='TCHR')
    serializer_class = UserTeacherListRelatedSerializer
    lookup_url_kwarg = 'pk2'

    def list(self, request, pk=None, *args, **kwargs):
        queryset = User.objects.filter(type_user=User.Type.TEACHER, school=pk)
        teacher_serializer = UserTeacherListRelatedSerializer(queryset, many=True)
        data = {
            "teachers": teacher_serializer.data
        }
        return Response(data)


