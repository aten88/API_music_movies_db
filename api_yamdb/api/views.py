from rest_framework import viewsets

from api.serializers import ReviewSerializer, CommentSerializer
from reviews.models import Review, Comment
from api.permissions import IsReviewOwnerOrReadOnly


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewOwnerOrReadOnly, ]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsReviewOwnerOrReadOnly, ]
