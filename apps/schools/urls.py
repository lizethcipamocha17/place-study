from django.urls import path, include
from apps.schools.api.views import views

# Django REST Framework
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'v1/schools', views.SchoolViewSet, basename='schools')
router.register(r'v1/schools/(?P<pk>[^/.]+)/teachers', views.TeacherViewSet, basename='teachers')
router.register(r'v1/schools/(?P<pk>[^/.]+)/contents', views.ContentViewSet, basename='contents')
# school/1/contents/1/coments
router.register(r'v1/schools/(?P<pk>[^/.]+)/contents/(?P<pk3>[^/.]+)/comments', views.CommentViewSet,
                basename='comments')

urlpatterns = [
    path('', include(router.urls))
]
