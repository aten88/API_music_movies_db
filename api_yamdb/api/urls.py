from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import CategoryViewSet, GenreViewSet, TitleViewSet
from api.views import (send_confirmation_code, get_jwt_token,
                       ReviewViewSet, CommentViewSet, UserViewSet)


router_v1 = DefaultRouter()
router_v1.register(r'categories', CategoryViewSet)
router_v1.register(r'genres', GenreViewSet)
router_v1.register(r'titles', TitleViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='review'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comment'
)
router.register(r'users', UserViewSet)

auth_patterns_v1 = [
    path('signup/', send_confirmation_code),
    path('token/', get_jwt_token)
]

urlpatterns = [
    path('v1/auth/', include(auth_patterns_v1)),
    path('v1/', include(router_v1.urls)),
]
