# Django REST framework
from django.shortcuts import _get_queryset
from rest_framework.exceptions import PermissionDenied, ParseError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, viewsets
# Models
from apps.accounts.api.serializers.users import UserTeacherListRelatedSerializer
from apps.accounts.models import User
from apps.schools.models import School, Content, Comment, Like
# Serializers
from apps.schools.api.serializers.serializers import (
    SchoolSerializer,
    ContentSerializer,
    CommentListSerializer,
    CommentCreateSerializer,
    LikeListSerializer, LikeUpdateSerializer)


# Create your views here.
class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

    def list(self, request, *args, **kwargs):
        """
        List all Schools
        """
        school_serializer = SchoolSerializer(self.queryset, many=True)
        return Response(school_serializer.data)


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


class ContentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ContentSerializer
    lookup_url_kwarg = 'pk3'

    def get_queryset(self, pk=None):
        school = self.request.user.school_id
        try:
            pk = int(pk)
        except Exception:
            raise ParseError(detail='Solicitud con formato incorrecto.')

        if school != pk:
            raise PermissionDenied(detail='No tienes permiso para realizar esta acción.')
        return Content.objects.filter(school_id=school)

    def list(self, request, pk=None, *args, **kwargs):
        """
        List all Contents for user loged and school
        """
        # obtener el colegio del usuario logeado  school_id
        # consulta a la tabla contenido filtrando el id del colegio
        content_serializer = ContentSerializer(self.get_queryset(pk), many=True)
        return Response(content_serializer.data)

    @action(detail=True, methods=['post', 'get'])
    def like(self, request, pk=None, *args, **kwargs):
        """
        Create like for content
        """
        # crear like se neceita decir a que content_id y que usuario es
        # quien da like, mas el like  # mostrar.........
        user = request.user
        if request.method == 'POST':
            serializer = LikeUpdateSerializer(user, data=request.data)
            serializer.is_valid(raise_exception=True)
            content, like = serializer.save()
            data = {
                'content': LikeListSerializer(content).data,
                'like': True
            }
            return Response({'data': data}, status=status.HTTP_201_CREATED)

        # else:
        #     likes = Like.objects.all().filter(content_id=pk)
        #     like_count = likes.count()
        #     serializer_class = LikeListSerializer(request.user, likes, many=True)
        #     return Response(serializer_class.data)

        # user = request.user.user_id
        # if request.method == 'POST':
        #     serializer = LikeUpdateSerializer(user, data=request.data)
        #     if serializer.is_valid():
        #         serializer.save()
        #         return Response(serializer.data, status=status.HTTP_201_CREATED)
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # else:
        #     likes = Like.objects.all().filter(content_id=pk)
        #     like_count = likes.count()
        #     serializer_class = LikeListSerializer(request.user, likes, many=True)
        #     return Response(serializer_class.data)


# school/1/contents/1/coments           PREGUNTAR EL ID SCHOOL EN EL ENDPORINT PERCHÉ??
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentListSerializer
    lookup_url_kwarg = 'pk4'

    #   traer el nombre de usuario (usuario logeado) que hace el comentario
    #   introducir(pedir) texto del comentario, id_contenido pedirlo
    def create(self, request, pk3=None, *args, **kwargs):
        """
        Create comment for content
        """
        print("PK3", pk3)
        content_model_viewset = ContentViewSet(request=request)
        content = content_model_viewset.retrieve(request, *args, **kwargs).data
        print("CONTENT", content)
        serializer = CommentCreateSerializer(context={'request': request, 'content': pk3}, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, pk3=None, *args, **kwargs):
        """
        List all Comments by content
        """

        queryset = Comment.objects.filter(content_id=pk3)
        comment_serializer = CommentListSerializer(queryset, many=True).data
        return Response(comment_serializer)
