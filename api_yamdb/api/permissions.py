from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsReviewOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.user == request.user
