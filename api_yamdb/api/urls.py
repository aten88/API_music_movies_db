from django.urls import include, path
from rest_framework import routers

from api.views import (send_confirmation_code, get_jwt_token,
                       ReviewViewSet, CommentViewSet)

router = routers.DefaultRouter()
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='review'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comment'
)

v1_auth_patterns = [
    path('signup/', send_confirmation_code),
    path('token/', get_jwt_token)
]

urlpatterns = [
    path('v1/auth/', include(v1_auth_patterns)),
    path('v1/', include(router.urls)),
]
