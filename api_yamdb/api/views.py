from rest_framework import viewsets
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

from api.serializers import ReviewSerializer, CommentSerializer
from reviews.models import Review, Comment
from api.permissions import IsReviewOwnerOrReadOnly
from api.utils import gen_send_mail
from api.serializers import RegisterDataSerializer, TokenSerializer

User = get_user_model()


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewOwnerOrReadOnly, ]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsReviewOwnerOrReadOnly, ]


@api_view(['POST'])
@permission_classes([AllowAny])
def send_confirmation_code(request):
    '''Вью-функция для регистрации нового пользователя,
    отвечает на запрос POST, создается экземпляр пользователя
    и присваивается код подтверждения, так же на почту
    пользователя отправляется сообщение с кодом подтверждения
    для получения токена jwt.'''
    serializer = RegisterDataSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    username = serializer.validated_data['username']
    email = serializer.validated_data['email']
    user = get_object_or_404(User, username=username, email=email)
    confirmation_code = default_token_generator.make_token(user)
    gen_send_mail(email, confirmation_code)
    user.confirmation_code = confirmation_code
    user.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_jwt_token(request):
    '''Вью-функция для получения зарегистрированным пользователем
    jwt токена.'''
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username']
    )

    if (user.confirmation_code
            == serializer.validated_data['confirmation_code']):
        token = AccessToken.for_user(user)
        return Response({"token": str(token)}, status=status.HTTP_200_OK)
