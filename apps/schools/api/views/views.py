# Django REST framework
from rest_framework.exceptions import PermissionDenied, ParseError, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, viewsets
# Models
from apps.accounts.models import User
from apps.schools.models import School, Content, Comment, Like
# Serializers
from apps.accounts.api.serializers.users import UserTeacherListRelatedSerializer
from apps.schools.api.serializers.serializers import (
    SchoolSerializer,
    ContentSerializer,
    CommentListSerializer,
    CommentCreateSerializer,
    LikeCreateSerializer)
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


class ContentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ContentSerializer
    lookup_url_kwarg = 'pk3'

    def get_queryset(self, pk=None, pk3=None):
        """This function returns a content filtered by a primary key"""
        school = self.request.user.school_id

        if school != parse_int(pk):
            raise PermissionDenied(detail='No tienes permiso para realizar esta acción.')

        queryset = Content.objects.filter(school_id=school)

        if pk3 is not None:
            pk3 = parse_int(pk3)
            queryset = queryset.filter(pk=pk3).first()
            if queryset is None:
                raise NotFound(detail='El contenido no existe o no tienes permiso para visualizarlo')
            return queryset

        return queryset

    def list(self, request, pk=None, *args, **kwargs):
        """
        Service for list all Contents for user loged and school
        """
        content_serializer = ContentSerializer(self.get_queryset(pk), many=True)
        return Response(content_serializer.data)

    def retrieve(self, request, pk=None, pk3=None, *args, **kwargs):
        """This function return a content"""
        content_serializer = ContentSerializer(self.get_queryset(pk, pk3))
        return Response(content_serializer.data)

    @action(detail=True, methods=['post', 'delete'])
    def like(self, request, pk=None, pk3=None, *args, **kwargs):
        """
        Service for create like for a content and return number likes
        """
        content = self.get_queryset(pk, pk3)
        if request.method == 'POST':
            serializer = LikeCreateSerializer(context={'request': request, 'content': content}, data=request.data)
            serializer.is_valid(raise_exception=True)
            like = serializer.save()
            likes = Like.objects.filter(content=content).count()
            data = {
                'content': ContentSerializer(content).data,
                'like': like.like,
                'likes': likes
            }
            return Response({'data': data}, status=status.HTTP_201_CREATED)

        else:
            like = Like.objects.filter(content=content, user=request.user).first()
            """Service for delete like and returns update number likes"""
            if like is None:
                raise ParseError('No haz reaccionado a este contenido')
            like.delete()
            likes = Like.objects.filter(content=content).count()
            data = {
                'content': ContentSerializer(content).data,
                'like': False,
                'likes': likes
            }
            return Response({'data': data}, status=status.HTTP_204_NO_CONTENT)


class UserContentsViewSet(viewsets.ModelViewSet):
    """
    UserContentsViewSet Used by users with teacher role
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ContentSerializer

    def get_queryset(self):
        return Content.objects.filter(school__user=self.request.user)

    def create(self, request, *args, **kwargs):
        if request.user.type_user != User.Type.TEACHER:
            raise PermissionDenied(detail="No tienes permiso para realizar esta acción")

        serializer = self.get_serializer(data=request.data, context={'school': request.user.school})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        if request.user.type_user != User.Type.TEACHER:
            raise PermissionDenied(detail="No tienes permiso para realizar esta acción")

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def update(self, request, *args, **kwargs):
        if request.user.type_user != User.Type.TEACHER:
            raise PermissionDenied(detail="No tienes permiso para realizar esta acción")

        content = self.get_object()
        partial = request.method == 'PATCH'
        serializer = self.get_serializer(content, data=request.data, partial=partial, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Contenido actualizado correctamente','data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """"""
        if request.user.type_user != User.Type.TEACHER:
            raise PermissionDenied(detail="No tienes permiso para realizar esta acción")
        content = self.get_object()
        content.delete()
        return Response({'message': 'El contenido fue eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentListSerializer
    lookup_url_kwarg = 'pk4'

    def create(self, request, pk=None, pk3=None, *args, **kwargs):
        """
        Service for create comment for content
        """
        content_model_viewset = ContentViewSet(request=request)
        content = content_model_viewset.get_queryset(pk=pk, pk3=pk3)
        serializer = CommentCreateSerializer(context={'request': request, 'content': content}, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, pk=None, pk3=None, *args, **kwargs):
        """
        Service for list all Comments by content
        """
        content_model_viewset = ContentViewSet(request=request)
        content = content_model_viewset.get_queryset(pk=pk, pk3=pk3)

        queryset = Comment.objects.filter(content=content)
        comment_serializer = CommentListSerializer(queryset, many=True).data
        return Response(comment_serializer)
