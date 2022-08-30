from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'api'

v1_router = DefaultRouter()
v1_router.register(
    'users',
    views.UsersViewSet,
    basename='users'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet,
    basename='reviews',
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='comments',
)
v1_router.register(
    r'categories',
    views.CategoryViewSet,
    basename='category'
)
v1_router.register(
    r'genres',
    views.GenreViewSet,
    basename='genre'
)
v1_router.register(
    r'titles',
    views.TitleViewSet,
    basename='title'
)

extra_patterns = [
    path('signup/', views.registration, name='registration'),
    path('token/', views.token, name='token'),
]

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/', include(extra_patterns)),
]
