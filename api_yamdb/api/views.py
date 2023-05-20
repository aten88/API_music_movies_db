from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, filters, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.pagination import PageNumberPagination

from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleSerializer, TitleWriteSerializer,
                             ReviewSerializer, CommentSerializer,
                             RegisterDataSerializer, TokenSerializer,
                             UserSerializer, UserProfileChangeSerializer,
                             InitialRegisterDataSerializer)
from api.filters import TitlesFilter
from api.permissions import IsAdminOrReadOnly, IsReviewOwnerOrReadOnly, IsAdmin
from reviews.models import Title, Category, Genre, Review, Comment
from api.utils import gen_send_mail


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    pass


User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def send_confirmation_code(request):
    '''Вью-функция для регистрации нового пользователя,
    отвечает на запрос POST, создается экземпляр пользователя
    и присваивается код подтверждения, так же на почту
    пользователя отправляется сообщение с кодом подтверждения
    для получения токена jwt. При повторном запросе пользователя,
    существующего в базе данных, код активации высылается на почту повторно.'''
    serializer = InitialRegisterDataSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.data['username']
    email = serializer.data['email']
    if User.objects.filter(username=username, email=email).exists():
        user = User.objects.get(username=username, email=email)
        confirmation_code = default_token_generator.make_token(user)
        gen_send_mail(user.email, confirmation_code)
        user.confirmation_code = confirmation_code
        user.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
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
    jwt токена при предъявлении кода подтверждения.'''
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
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    '''Вью-функция для администрирования пользователей.
    Доступ открыт только для админимтраторов и суперюзеров.
    Реализован поиск по полю username.
    Реализована возможность любому аутентифицированному
    пользователю просматривать и изменять данные своей учетной записи.'''
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )
    pagination_class = PageNumberPagination

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)

    @action(
        methods=['get', 'patch'],
        detail=False,
        url_path='me',
        permission_classes=[IsAuthenticated],
        serializer_class=UserProfileChangeSerializer
    )
    def user_profile_change(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return TitleWriteSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewOwnerOrReadOnly, ]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsReviewOwnerOrReadOnly, ]
