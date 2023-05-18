from rest_framework import serializers
from reviews.models import Review, Comment
from django.contrib.auth import get_user_model

User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class RegisterDataSerializer(serializers.ModelSerializer):
    '''Сериализатор для данных регистрации. Добавлена валидация по
    полю username, исключающая возможность использования me как логина'''

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
