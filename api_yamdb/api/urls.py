from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views


v1_router = DefaultRouter()
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet,
    basename="reviews",
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename="comments",
)

urlpatterns = [
    path('', include(v1_router.urls)),
]