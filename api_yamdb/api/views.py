from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.serializers import ReviewSerializer, CommentSerializer
from reviews.models import Review, Comment


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
