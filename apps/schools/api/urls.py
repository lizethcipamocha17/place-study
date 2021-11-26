from django.urls import path, include
from apps.schools.api.views import views

# Django REST Framework
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'v1/schools', views.SchoolViewSet, basename='schools')
router.register(r'v1/schools/(?P<pk>[^/.]+)/teachers', views.TeacherViewSet, basename='teachers')
router.register(r'v1/schools/(?P<pk>[^/.]+)/contents', views.ContentViewSet, basename='contents')
router.register(r'v1/schools/(?P<pk>[^/.]+)/contents/(?P<pk3>[^/.]+)/comments', views.CommentViewSet,
                basename='comments')
router.register(r'v1/contents', views.UserContentsViewSet, basename='user-contents')
# router.register(r'v1/admin/schools/(?P<pk>[^/.]+)/teachers/(?P<pk2>[^/.]+)/contents')

urlpatterns = [
    path('', include(router.urls))
]
