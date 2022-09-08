from django.urls import path, include
from apps.contents.api.views import content_view

# Django REST Framework
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'v1/schools/(?P<pk>[^/.]+)/contents', content_view.ContentViewSet, basename='contents')
router.register(r'v1/schools/(?P<pk>[^/.]+)/schools/(?P<pk3>[^/.]+)/comments', content_view.CommentViewSet,
                basename='comments')
router.register(r'v1/contents', content_view.UserContentsViewSet, basename='user-contents')

urlpatterns = [
    path('', include(router.urls))
]