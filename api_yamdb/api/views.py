from api.permissions import AdminOrReadOnly, IsAuthorOrReadOnly
from api.serializers import (AdminsSerializer, CategorySerializer,
                             CommentSerializer, GenreSerializer,
                             ReviewSerializer, TitleSerializer,
                             UsersSerializer)

from rest_framework import viewsets, filters, status, permissions
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django_filters import CharFilter, FilterSet, NumberFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from reviews.models import Category, Genre, Review, Title, User
from rest_framework import mixins, generics
from reviews.models import Review, Title, Genre, Category, User
from api.permissions import IsAuthorOrReadOnly, AdminOrReadOnly
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import AccessToken

from api.serializers import (
    AdminsSerializer, UsersSerializer,
    ReviewSerializer, CommentSerializer,
    TitleSerializer, CategorySerializer, GenreSerializer,
    RegistrationSerializer, TokenSerializer)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def registration(request):
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username']
    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Регистрация на YaMDB',
        message=f'Ваш код подтверждения: {confirmation_code}',
        from_email=None,
        recipient_list=[user.email],
    )

    return Response(serializer.data, status=status.HTTP_200_OK)

#не получается зарегистрироваться

@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data["username"]
    )

    if default_token_generator.check_token(
        user, serializer.validated_data["confirmation_code"]
    ):
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# не получается получить токен

class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    lookup_field = 'username'
    search_fields = ('username', )

    @action(
        methods=['PATCH', 'GET'],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path='me')
    def get_current_user_info(self, request):
        serializer = UsersSerializer(request.user)
        if request.method == 'PATCH':
            if request.user.is_administrator():
                serializer = AdminsSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            else:
                serializer = UsersSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)


class TitleFilterSet(FilterSet):
    # Фильтры на Title:
    # category (фильтрует по полю slug категории),
    # genre (фильтрует по полю slug жанра),
    # name(фильтрует по названию произведения),
    # year(фильтрует по году)
    # https://django-filter.readthedocs.io/en/stable/ref/filters.html

    category = CharFilter(field_name='category__slug')
    genre = CharFilter(field_name='genre__slug')
    name = CharFilter(field_name='name')
    year = NumberFilter(field_name='year')

    class Meta:
        model = Title
        fields = ['category', 'genre', 'name', 'year']


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')).order_by('id')
    serializer_class = TitleSerializer
    permission_classes = [AdminOrReadOnly]
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = TitleFilterSet
    ordering_fields = ('name', 'year')
    def perform_create(self, serializer):
        category = generics.get_object_or_404(
            Category, slug=self.request.data.get("category")
        )
        genre = Genre.objects.filter(
            slug__in=self.request.data.getlist("genre")
        )
        serializer.save(category=category, genre=genre)

    def perform_update(self, serializer):
        self.perform_create(serializer)


class CreateDestroyListViewSet(
    # Набор представлений, который по умолчанию
    # предоставляет операции «create ()», «destroy ()» и «list ()».
    # https://russianblogs.com/article/84681093457/
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    pass


class CategoryViewSet(CreateDestroyListViewSet):
    lookup_field = 'slug'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AdminOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    # Поиск по названию категории
    search_fields = ('name',)
    ordering = ('name',)


class GenreViewSet(CreateDestroyListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [AdminOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    # Поиск по названию жанра
    search_fields = ('name',)
