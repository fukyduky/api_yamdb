from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

from .views import ReviewViewSet, CommentViewSet


v1_router = DefaultRouter()
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews',
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)
v1_router.register(r'categories', 
    views.CategoryViewSet,
    basename='category'
)
v1_router.register(r'genres',
    views.GenreViewSet,
    basename='genre'
)
v1_router.register(r'titles',
    views.TitleViewSet,
    basename='title'
)

urlpatterns = [
    path('/v1/', include(v1_router.urls)),
]
