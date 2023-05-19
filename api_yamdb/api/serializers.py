from rest_framework import serializers
from django.contrib.auth import get_user_model

from reviews.models import Review, Comment

User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('title', 'author', 'text', 'score', 'created_at')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('review', 'author', 'text', 'created_at')


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
