from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
<<<<<<< HEAD
from reviews.models import Category, Comment, Genre, Review, Title, User
=======
from rest_framework.validators import UniqueValidator


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    username = serializers.CharField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Нельзя использовать "me" как имя пользователя')
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    confirmation_code = serializers.CharField(max_length=150)
>>>>>>> ada565068263a13ced17cb7787a010c0e48c6b52


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token), }


class EmailAuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    confirmation_code = serializers.CharField(max_length=150)

    def validate(self, data):
        user = get_object_or_404(
            User, confirmation_code=data['confirmation_code'],
            email=data['email']
        )
        return get_tokens_for_user(user)


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email',
            'bio', 'role', 'confirmation_code')
        read_only_field = ('role',)


class AdminsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email',
            'bio', 'role', 'confirmation_code')



class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )


    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field="slug",
        many=True,
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "description",
            "genre",
            "category",
        )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ("id",)
        lookup_field = "slug"


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')
