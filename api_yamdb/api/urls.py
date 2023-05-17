from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import CategoryViewSet, GenreViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]
