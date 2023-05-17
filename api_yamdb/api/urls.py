from django.urls import include, path
from rest_framework import routers
from api.views import ReviewViewSet, CommentViewSet

router = routers.DefaultRouter()
router.register(r'reviews', ReviewViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('api/v1', include(routers.urls)),

]
