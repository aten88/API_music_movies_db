from datetime import datetime

from django.contrib.auth import get_user_model
from rest_framework import serializers

from reviews.models import Category, Genre, Title, Review, Comment


User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True)
    genre = GenreSerializer(many=True, source='genres')
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects, slug_field='slug')
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects, slug_field='slug', many=True, source='genres')

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')

    def validate_year(self, value):
        if not 0 < value <= datetime.now().year:
            raise serializers.ValidationError('Некорректно указан год выпуска')
        return value


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'author', 'text', 'score', 'pub_date')

    def validate(self, data):
        if self.context['request'].method == 'POST':
            author = self.context['request'].user
            title = self.context['view'].kwargs.get('title_id')
            if Review.objects.filter(author=author, title=title).exists():
                raise serializers.ValidationError(
                    'Нельзя дважды оценить одно произведение')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'pub_date')


class InitialRegisterDataSerializer(serializers.Serializer):
    '''Сериализатор входящих данных пользователя.
    Реализует повторную отправку кода подтвержджения для
    существующего юзера.'''
    username = serializers.CharField()
    email = serializers.EmailField()


class RegisterDataSerializer(serializers.ModelSerializer):
    '''Сериализатор для данных регистрации. Добавлена валидация по
    полю username, исключающая возможность использования me как логина.'''

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать \'me\' в качестве логина')
        return value

    class Meta:
        fields = ('username', 'email')
        model = User


class TokenSerializer(serializers.Serializer):
    '''Сериализатор для получения токена jwt.'''
    confirmation_code = serializers.CharField()
    username = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    '''Сериализатор данных пользователя.'''

    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = User


class UserProfileChangeSerializer(serializers.ModelSerializer):
    '''Сериализатор данных пользователя. Используется при
    внесении самим пользователем изменений в профиль,
    запрещено изменение поля role.'''

    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = User
        read_only_fields = ('role', )
